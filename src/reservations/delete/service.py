import boto3
import json
from custom_encoder import CustomEncoder
import logging
import os
import datetime

TABLE_NAME = os.environ.get("TABLE_NAME")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Service:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    @classmethod
    def deleteReservation(cls, reservation_id: str, timestamp) -> dict:
        try:
            response = cls.table.update_item(
            Key={
                    'reservation_id': reservation_id,
                    'timestamp': timestamp
                },                UpdateExpression="set deleted = :deleted, last_updated = :last_updated",
                ExpressionAttributeValues={
                    ':deleted': 1,
                    ':last_updated': datetime.datetime.now().isoformat()
                },
                ReturnValues="ALL_NEW"
            )
            body = {
                'Operation': 'DELETE',
                'Message': 'SUCCESS',
                'Item': response['Attributes']
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
        