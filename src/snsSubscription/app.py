from service import Service
import json

def lambda_handler(event, context):
    requestBody = json.loads(event['body'])
    email_address = requestBody['email']
    service = Service()   

    service.create_subscription(email_address)
    body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS'
    }
    return  Service.buildResponse(200,body)
    
