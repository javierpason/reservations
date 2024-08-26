import json
import boto3
from botocore.exceptions import ClientError

eventbridge = boto3.client('events')

def lambda_handler(event, context):
    try:
        if 'Records' not in event:
            raise ValueError("Event does not contain 'Records' key")
            
        for record in event['Records']:
            if record['eventName'] in ['INSERT', 'MODIFY', 'REMOVE']:
                event_detail = {
                    'eventName': record['eventName'],
                    'dynamodb': record['dynamodb']
                }
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
               
        return {
            'statusCode': 200,
            'body': json.dumps('Processed records successfully!')
        }
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