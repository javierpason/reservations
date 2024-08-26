import boto3
import json
from custom_encoder import CustomEncoder
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
eventbridge = boto3.client('events')


class Service:
    @classmethod
    def create_eventbridge_message(cls,event_detail: str) -> None:
        # Emit an event to EventBridge
        eventbridge.put_events(
            Entries=[
                {
                    'Source': 'loanpro.reservation.service',
                    'DetailType': 'ReservationCreated',
                    'Detail': json.dumps(event_detail),
                    'EventBusName': 'default'  # Use a custom event bus if needed
                }
            ]
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
        