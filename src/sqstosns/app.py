import json
import boto3

def lambda_handler(event, context):
    sns = boto3.client('sns')
    print(event)
    # Replace with your topic ARN
    topic_arn = 'arn:aws:sns:us-east-1:339712723054:reservation-topic'
    
    for record in event['Records']:
        message_body = json.loads(record['body'])
        
        detail = message_body.get('detail', {})
        new_image = detail.get('dynamodb', {}).get('NewImage', {})
        user = new_image.get('user', {}).get('S', 'unknown user')
        reservation_id = new_image.get('reservation_id', {}).get('S', 'unknown user')
        status = new_image.get('reservation_status', {}).get('S', 'unknown status')
        timestamp = new_image.get('created', {}).get('S', 'unknown timestamp')
        formatted_message = f"Hello {user}, your reservation has been {status} the day {timestamp}."
        message = f"Message from SQS , reservation {reservation_id}."
        
        response = sns.publish(
            TopicArn=topic_arn,
            Message=formatted_message,
            Subject=message
        )
    
        print("user => ",user)
   
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to SNS topic')
    }
