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

def delete_task_handler(event, context):
    try:
        logger.info("Starting function")
        # リクエストボディの解析
        body = json.loads(event['body'])
        
        user_id = body['userId']
        task_id = body['taskId']
        
        # タスクを削除
        response = table.delete_item(
            Key={
                'PK': user_id,
                'SK': task_id
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS,PUT,POST,DELETE",
                "Access-Control-Allow-Headers": "Content-Type,",
            },
            'body': json.dumps({'message': 'Task deleted successfully'})
        }
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to delete task', 'error': str(e)})
        }
