import boto3
import uuid
import json
from custom_encoder import CustomEncoder
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodbTableName = 'reservations'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthPath =  '/health'
reservationPath = '/reservations'
reservationsPath = '/reservations'
usersPath = '/Users'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)  
    elif httpMethod == getMethod and path == reservationPath:
        response = getReservation(event['queryStringParameters']['reservation_id'],event['queryStringParameters']['timestamp'])
    elif httpMethod == getMethod and path == reservationPath:
        response = getReservations()
    elif httpMethod == postMethod and path == reservationPath:
        response = saveReservation(json.loads(event['body']))
    elif httpMethod == patchMethod and path == reservationPath:
        requestBody = json.loads(event['body'])
        response = modifyReservation(requestBody['reservation_id'],requestBody['timestamp'],requestBody['updateKey'],requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == reservationPath:
        response = deleteReservation(requestBody['reservation_id'])
    else:
        response = buildResponse(404, 'Not Found')

    return response

def getReservation(reservation_id,timestamp):
    try:
        response = table.get_item(
            Key={
                'reservation_id': reservation_id,
                'timestamp': timestamp       
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'reservation_id: %s not found' % reservation_id})
    except:
        logger.exception('Do your custom code error handling here. I am just gonna log it out here!!')


def getReservations():
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'products': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom code error handling here. I am just gonna log it out here!!')

def saveReservation(requestBody):
    try:
        reservation_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()

        reservation_data = {
            'reservation_id': reservation_id,
            'user': requestBody['user'],
            'details': requestBody['details'],
            'status': 'created',
            'timestamp': timestamp
        }
        table.put_item(Item=reservation_data)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': reservation_data
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom code error handling here. I am just gonna log it out here!!')

def modifyReservation(reservation_id, timestamp, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'reservation_id': reservation_id,
                'timestamp': timestamp     
            },
            UpdateExpression='set %s = :value' % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAtributes': response
        }
        return buildResponse(200,body)
    except:
        logger.exception('Do your custom code error handling here. I am just gonna log it out here!!')

def deleteReservation(reservation_id):
    try:
        response = table.delete_item(
            Key={
                'reservation_id': reservation_id
            },
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response        
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom code error handling here. I am just gonna log it out here!!')

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Heders': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response