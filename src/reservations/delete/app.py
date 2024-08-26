from service import Service
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    service = Service()   

    path_parameters = event.get('pathParameters', {})
    reservation_id = path_parameters.get('reservation_id')
    timestamp = path_parameters.get('timestamp')

    response = service.deleteReservation(reservation_id,timestamp)

    return Service.buildResponse(statusCode=200,body=response)

