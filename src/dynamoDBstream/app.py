import json
import boto3
from botocore.exceptions import ClientError
from service import Service

eventbridge = boto3.client('events')

def lambda_handler(event, context):
    try:
        if 'Records' not in event:
            raise ValueError("Event does not contain 'Records' key")

        service = Service()   
        for record in event['Records']:
            if record['eventName'] in ['INSERT', 'MODIFY', 'REMOVE']:
                event_detail = {
                    'eventName': record['eventName'],
                    'dynamodb': record['dynamodb']
                }

                service.create_eventbridge_message(event_detail=event_detail)   
        
        body = {
            'Operation': 'SAVE',
            'Message': 'Message saved in EventBridge'
         }
        return  Service.buildResponse(200,body)
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error creating reservation: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Unexpected error: {str(e)}'})
        }