import json
import os 
import boto3
import logging
import uuid
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
        return super(DecimalEncoder).default(obj)
    
def update_todo_handler(event, context):
    try:
        logger.info("Starting function")
        # リクエストボディの解析
        body = json.loads(event['body'])
        
        user_id = body['userId']
        todo_id = body.get('todoId')
        title = body['title']
        target_date = body['targetDate']
        budget = body['budget']
        completed = body['completed']
        tasks = body['tasks'] # タスクのリスト
        
        # ToDoアイテムの更新
        response = table.update_item(
            Key={
                'PK': user_id,
                'SK': todo_id
            },
            UpdateExpression="set #title = :title, #target_date = :target_date, #budget = :budget, #completed = :completed",
            ExpressionAttributeNames={
                '#title': 'Title',
                '#target_date': 'TargetDate',
                '#budget': 'Budget',
                '#completed': 'Completed'
            },
            ExpressionAttributeValues={
                ':title': title,
                ':target_date': target_date,
                ':budget': budget,
                ':completed': completed
            },
            ReturnValues="UPDATED_NEW"
        )
        
        # 新しいタスクの追加および既存タスクの更新
        with table.batch_writer() as batch:
            for task in tasks:
                task_id = task.get('taskId')
                if not task_id:
                    # 新しいタスクの場合、uuidを生成
                    task_id = str(uuid.uuid4())
                    task_id = f'{todo_id}#TASK#{task_id}'
                else:
                    # 既存のtask_idに余分なプレフィックスが追加されないように確認
                    if not task_id.startswith(f'{todo_id}#TASK#'):
                        task_id = f'{todo_id}#TASK#{task_id}'
                        
                task_item = {
                    'PK': user_id,
                    'SK': task_id,
                    'Title': task['title'],
                    'TargetDate': task['targetDate'],
                    'Completed': task['completed']
                }
                batch.put_item(Item=task_item)
                
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'ToDo and tasks updated successfully'}, cls=DecimalEncoder)
        }
    except Exception as e:
        logger.error(f"Error updating ToDo and tasks: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to update ToDo and tasks', 'error': str(e)})
        }