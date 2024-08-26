import boto3
import json
from custom_encoder import CustomEncoder
import logging
import os

TABLE_NAME = os.environ.get("TABLE_NAME")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Service:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
   
    @classmethod
    def getReservation(cls, reservation_id:str,timestamp:int)-> dict | None:
        try:
            response = cls.table.get_item(
                Key={
                    'reservation_id': reservation_id,
                    'timestamp': timestamp       
                }
            )
            return response.get('Item',None)                
            
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
        