import boto3
import json
from custom_encoder import CustomEncoder
import logging
import os

TABLE_NAME = os.environ.get("TABLE_NAME")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Service:
    @classmethod
    def create_subscription(cls,email_address: str) -> None:
        sns_client = boto3.client('sns')
        
        
        TOPIC_NAME = os.environ.get("TOPIC_NAME")
        topic_arn = TOPIC_NAME
        
        # Create the SNS subscription
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )


    @staticmethod    
    def buildResponse(statusCode, body):
        response = {
            'statusCode': statusCode,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Heders': '*'
            },
            'body': json.dumps(body,cls=CustomEncoder)
        }
       
        return response
        