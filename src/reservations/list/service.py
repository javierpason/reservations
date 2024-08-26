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
    def getReservations(cls)->list:
        records = []
        try:
            response = cls.table.scan()
            records = response['Items']
            
            while 'LastEvaluatedKey' in response:
                response = cls.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                records.extend(response['Items'])
           
        except:
            logger.exception('Do your custom code error handling here. I am just gonna log it out here!!')
        
      
        return records
    
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
        