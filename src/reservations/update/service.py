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
    def modifyReservation(cls, reservation_id, timestamp, updates):
        try:
            # Construct the UpdateExpression and ExpressionAttributeValues
            update_expression = "set "
            expression_attribute_values = {}
            updates['reservation_status'] = 'Updated'
            
            # Build the UpdateExpression and ExpressionAttributeValues
            for index, (key, value) in enumerate(updates.items()):
                if index > 0:
                    update_expression += ", "
                update_expression += f"{key} = :value{index}"
                expression_attribute_values[f":value{index}"] = value

            # Perform the update operation
            response = cls.table.update_item(
                Key={
                    'reservation_id': reservation_id,
                    'timestamp': timestamp
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues='UPDATED_NEW'
            )

            body = {
                'Operation': 'UPDATE',
                'Message': 'SUCCESS',
                'UpdatedAttributes': response.get('Attributes', {})
            }
            return body
        except Exception as e:
            logger.exception('Error updating reservation')
            raise e

    # @classmethod
    # def modifyReservation(cls,reservation_id, timestamp, updateKey, updateValue):
    #     try:
    #         response = cls.table.update_item(
    #             Key={
    #                 'reservation_id': reservation_id,
    #                 'timestamp': timestamp     
    #             },
    #             UpdateExpression='set %s = :value' % updateKey,
    #             ExpressionAttributeValues={
    #                 ':value': updateValue
    #             },
    #             ReturnValues='UPDATED_NEW'
    #         )
    #         body = {
    #             'Operation': 'UPDATE',
    #             'Message': 'SUCCESS',
    #             'UpdatedAtributes': response
    #         }
    #         return body
    #     except:
    #         logger.exception('Do your custom code error handling here. I am just gonna log it out here!!')

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
        