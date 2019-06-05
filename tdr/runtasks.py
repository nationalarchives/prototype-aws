import json
import boto3
import os


def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    message = sqs_client.send_message(
        QueueUrl=os.environ['QUEUE_URL'], MessageBody=json.dumps(event))

    ecs_client = boto3.client('ecs')

    ecs_client.run_task(cluster='default', taskDefinition=os.environ['TASK_ARN'], launchType="FARGATE", networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                os.environ['SUBNET_ID'],
            ],
            'securityGroups': [
                os.environ['SECURITY_GROUP_ID'],
            ],
            'assignPublicIp': 'ENABLED'
        }
    }
    )
