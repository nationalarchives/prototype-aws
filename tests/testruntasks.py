import unittest
import tdr.runtasks
import boto3
from moto import mock_ecs, mock_sqs, mock_ec2
import json
import os


class TestRunTasks(unittest.TestCase):

    def setUp(self):
        os.environ["QUEUE_URL"] = "testqueue"

    def setup_ec2(self):
        ec2 = boto3.resource("ec2", region_name='eu-west-2')
        response = ec2.create_instances(
            ImageId='<ami-image-id>', MinCount=1, MaxCount=5)
        return response[0].id

    def setup_sqs(self):
        sqs_client = boto3.client('sqs', region_name='eu-west-2')
        sqs_client.create_queue(QueueName='testqueue')
        return sqs_client

    def setup_ecs(self):
        os.environ['SUBNET_ID'] = 'subnet'
        os.environ['SECURITY_GROUP_ID'] = 'sgid'

        ecs_client = boto3.client('ecs', region_name='eu-west-2')
        response = ecs_client.create_cluster(
            clusterName='default',
        )
        instance_id = self.setup_ec2()
        ecs_client.register_container_instance(
            cluster='default', instanceIdentityDocument=json.dumps({"region": "eu-west-2", "instanceId": instance_id}))

        with open('tests/task-definition.json', 'r') as definition:
            task = json.loads(definition.read())
            response = ecs_client.register_task_definition(
                **task['taskDefinition'])
            os.environ["TASK_ARN"] = response['taskDefinition']['taskDefinitionArn']
        return ecs_client

    @mock_sqs
    @mock_ecs
    @mock_ec2
    def test_run_lambda(self):

        test_event = {
            "file": "testfile"
        }
        sqs_client = self.setup_sqs()
        ecs_client = self.setup_ecs()

        tdr.runtasks.lambda_handler(test_event, None)

        messages = sqs_client.receive_message(QueueUrl='testqueue')
        self.assertEqual(messages['Messages'][0]
                         ['Body'], json.dumps(test_event))

        self.assertGreater(
            len(ecs_client.list_tasks(
                desiredStatus='RUNNING')['taskArns']), 0)
