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

def delete_todo_handler(event, context):
    try:
        logger.info("Starting function")
        # リクエストボディの解析
        body = json.loads(event['body'])
        
        user_id = body['userId']
        todo_id = body['todoId']
        
        # ToDoに紐づく全てのタスクを取得
        tasks_response = table.query(
            KeyConditionExpression="PK = :pk and begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ':pk': user_id,
                ':sk_prefix': f'{todo_id}#TASK#'
            }
        )
        tasks = tasks_response.get('Items', [])
        
        # ToDoとタスクを削除
        with table.batch_writer() as batch:
            # ToDoを削除
            batch.delete_item(
                Key={
                    'PK': user_id,
                    'SK': todo_id
                }
            )
            # タスクを削除
            for task in tasks:
                batch.delete_item(
                    Key={
                        'PK': task['PK'],
                        'SK': task['SK']
                    }
                )
                
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'ToDo and tasks deleted successfully'})
        }
    except Exception as e:
        logger.error(f'Error deleting ToDo and tasks: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to delete ToDo and tasks', 'error': str(e)})
        }