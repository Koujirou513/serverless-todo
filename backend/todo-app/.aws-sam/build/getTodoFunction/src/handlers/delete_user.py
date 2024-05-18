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

def delete_user_handler(event, context):
    try:
        logger.info("Starting function")
        # リクエストボディの解析
        body = json.loads(event['body'])
        
        user_id = body['userId']
        
        response = table.delete_item(
            Key={
                'PK': f'USER#{user_id}',
                'SK': f'USER#{user_id}'
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    except Exception as e:
        logger.error(f'Error deleting user: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to delete user', 'error': str(e)})
        }