import json
import boto3
import os
import logging
from decimal import Decimal

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

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
    
def task_completed_handler(event, context):
    try:
        logger.info("Starting function")
        # リクエストボディの解析
        body = json.loads(event['body'])
        
        user_id = body['userId']
        task_id = body['taskId']
        
        # タスクの現在のCompleted状態を取得
        response = table.get_item(
            Key={
                'PK': user_id,
                'SK': task_id
            }
        )
        task = response.get('Item', {})
        
        if not task:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }
        
        current_completed = task['Completed']
        new_completed = not current_completed 
        
        # Completed状態のトグル
        response = table.update_item(
            Key={
                'PK': user_id,
                'SK': task_id
            },
            UpdateExpression="set #completed = :completed",
            ExpressionAttributeNames={
                '#completed': 'Completed'
            },
            ExpressionAttributeValues={
                ':completed': new_completed
            },
            ReturnValues="UPDATED_NEW"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'massage': 'Task completed state toggled successfully', 'newCompleted': new_completed}, cls=DecimalEncoder)
        }
    except Exception as e:
        logger.error(f"Error toggling task completed state: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to toggle task completed state', 'error': str(e)})
        }
            
        