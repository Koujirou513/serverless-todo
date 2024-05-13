import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = os.environ.get('TABLE_NAME')
dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')

# DynamoDBリソースの初期化
if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(table_name)

def getAllItemsHandler(event, context):
    try:
        logger.info("Starting function")
        
        response = table.scan(
            FilterExpression="begins_with(PK, :pk_prefix) and begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ':pk_prefix': 'USER#',
                ':sk_prefix': 'USER#'
            }
        )
        items = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps({'users': items})
        }
        
    except Exception as e:
        logger.error(f'Error retrieving data: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to fetch user data', 'error': str(e)})
        }
