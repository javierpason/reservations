from service import Service
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    service = Service()
   
    body = json.loads(event['body'])
        
    # Extract necessary fields from the request body
    reservation_id = body.get('reservation_id')
    timestamp = body.get('timestamp')
    updates = body.get('updates', {})
   
    response = service.modifyReservation(reservation_id, timestamp, updates)

    return Service.buildResponse(statusCode=200,body=response)


# def parse_request(event):
#     requestBody = json.loads(event['body'])
#     reservation_id = requestBody['reservation_id']
#     timestamp = requestBody['timestamp']
#     updatekey =  requestBody['updateKey']
#     updateValue = requestBody['updateValue']
#     return n,n,n,n,n,n,