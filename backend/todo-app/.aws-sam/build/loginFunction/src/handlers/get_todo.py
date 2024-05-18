import json
import os 
import boto3
from decimal import Decimal

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

def get_todo_handler(event, context):
    try:
        # クエリパラメータからユーザーIDを取得
        user_id = event['queryStringParameters']['userId']
        todo_id = event['queryStringParameters']['todoId']
        
        # DynamoDBから特定のToDo情報を取得
        response = table.get_item(
            TableName=table_name,
            Key={
                'PK': f'USER#{user_id}',
                'SK': todo_id
            }
        )
        
        todo = response.get('Item', {})
        
        if not todo:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
        # ToDoに紐づく全てのタスクを取得
        tasks_response = table.query(
            KeyConditionExpression="PK = :pk and begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ':pk': f'USER#{user_id}',
                ':sk_prefix': f'{todo_id}#TASK#'
            }
        )
        tasks = tasks_response.get('Items', [])
        
        # レスポンスの生成
        result = {
            'todo': todo,
            'tasks': tasks
        }
            
        
        return {
            'statusCode': 200,
            'body': json.dumps(result, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error retrieving user data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to fetch user data', 'error': str(e)})
        }