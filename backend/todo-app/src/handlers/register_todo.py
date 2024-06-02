import json
import os
import boto3
import uuid

# 環境変数から情報を取得
table_name = os.environ.get('TABLE_NAME')
dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')

# DynamoDBリソースの初期化
if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(table_name)

def register_todo_handler(event, context):
    try:
        #リクエストボディの解析
        body = json.loads(event['body'])
        
        user_id = body['userId']
        title = body['title']
        target_date = body['targetDate']
        budget = body['budget']
        completed = body['completed']
        tasks = body['tasks']  #中間目標のリスト
        
        # 空のタスクを除外
        filtered_tasks = [task for task in tasks if task['title'] and task['targetDate']]
        
        # Todoアイテムの生成
        todo_id = str(uuid.uuid4())
        todo_item = {
            'PK': user_id,
            'SK': f'TODO#{todo_id}',
            'Title': title,
            'TargetDate': target_date,
            'Budget': budget,
            'Completed': completed
        }
        
        # DynamoDBに書き込むアイテムのリスト
        items = [todo_item]
        
        #中間目標アイテムの生成
        for task in filtered_tasks:
            task_id = str(uuid.uuid4())
            task_item = {
                'PK': user_id,
                'SK': f'TODO#{todo_id}#TASK#{task_id}',
                'Title': task['title'],
                'TargetDate': task['targetDate'],
                'Completed': task['completed']
            }
            items.append(task_item)
            
        # Batch書き込み
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
                
        # レスポンスの生成
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS,PUT,POST,DELETE",
                "Access-Control-Allow-Headers": "Content-Type,",
            },
            'body': json.dumps({'message': 'ToDo and tasks registered successfully'})
        }
    except Exception as e:
        print(f"Error registering ToDo and tasks: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to register ToDo and tasks', 'error': str(e)})
        }
