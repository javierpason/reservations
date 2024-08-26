from service import Service
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    service = Service()
    
    response = service.saveReservation(requestBody=json.loads(event['body'])) 
    return Service.buildResponse(statusCode=200,body=response)


  