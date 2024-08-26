import boto3
import json
from custom_encoder import CustomEncoder
import logging
import os
import datetime
import uuid

TABLE_NAME = os.environ.get("TABLE_NAME")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Service:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    @classmethod
    def saveReservation(cls, requestBody:dict) -> dict:
        try:
            reservation_id = str(uuid.uuid4())
            created = datetime.datetime.now().isoformat()
            timestamp = datetime.datetime.now().timestamp()
            reservation_data = {
                'reservation_id': reservation_id,
                'user': requestBody['user'],
                'details': requestBody['details'],
                'reservation_status': 'created',
                'timestamp': int(timestamp),
                'deleted': 0,
                'created': created,
                'last_updated': created
            }
            cls.table.put_item(Item=reservation_data)
            body = {
                'Operation': 'SAVE',
                'Message': 'SUCCESS',
                'Item': reservation_data
            }
            return body
        except Exception as e:
         logger.exception(e)
         raise e

    
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
        