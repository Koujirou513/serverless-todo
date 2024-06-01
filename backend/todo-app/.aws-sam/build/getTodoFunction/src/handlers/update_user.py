import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数から情報を取得
table_name = os.environ.get('TABLE_NAME')
dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')

# DynamoDBリソースの初期化
if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(table_name)


def update_user_handler(event, context):
    try:
        logger.info("Starting function")
        # リクエストボディの解析
        body = json.loads(event['body'])
        
        user_id = body['userId']
        new_name = body['newName']
        
        response = table.update_item(
            Key={
                'PK': user_id,
                'SK': user_id
            },
            UpdateExpression="set #name = :new_name",
            ExpressionAttributeNames={
                '#name': 'Name'
            },
            ExpressionAttributeValues={
                ':new_name': new_name
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS,PUT,POST,DELETE",
                "Access-Control-Allow-Headers": "Content-Type,",
            },
            'body': json.dumps({'message': 'User name updated successfully', 'newName': new_name})
        }
    except Exception as e:
        logger.error(f"Error updating user name: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to update user name', 'error': str(e)})
        }