import json
import boto3
import os


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    sqs_client.send_message(
        QueueUrl=os.environ['QUEUE_URL'], MessageBody=json.dumps(event))
    attr = sqs_client.get_queue_attributes(
        QueueUrl=os.environ['QUEUE_URL'], AttributeNames=['ApproximateNumberOfMessages'])

    ecs_client = boto3.client('ecs')
    tasks = ecs_client.list_tasks()['taskArns']
    if int(attr['Attributes']['ApproximateNumberOfMessages']) > 50 or len(tasks) < 3 or len(tasks) == 0:
        ecs_client.run_task(taskDefinition=os.environ['TASK_ARN'], launchType="FARGATE", networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    os.environ['SUBNET_ID'],
                ],
                'securityGroups': [
                    os.environ['SECURITY_GROUP_ID'],
                ],
                'assignPublicIp': 'ENABLED'
            }
        })


lambda_handler(None, None)
