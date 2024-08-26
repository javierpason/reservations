from service import Service
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    service = Service()
    status_code = 200
    
    response = service.getReservation(event.get('pathParameters').get('reservation_id'),int(event.get('pathParameters').get('timestamp')))
    
    if response is None:
        status_code = 404
        response = "Not found"
    
    return Service.buildResponse(statusCode=status_code,body=response)


  

