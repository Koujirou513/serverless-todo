import json
import os 
import boto3

# 環境変数から情報を取得
table_name = os.environ.get('TABLE_NAME')
dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')

# DynamoDBリソースの初期化
if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(table_name)

def get_user_handler(event, context):
    try:
        # クエリパラメータからユーザーIDを取得
        user_id = event['queryStringParameters']['userId']
        
        # DynamoDBからユーザー情報を取得
        response = table.get_item(
            TableName=table_name,
            Key={
                'PK': user_id,
                'SK': user_id
            }
        )
        
        item = response.get('Item', {})
        
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
            
        # パスワードをレスポンスから削除
        item.pop('Password', None)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'user': item})
        }
        
    except Exception as e:
        print(f"Error retrieving user data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to fetch user data', 'error': str(e)})
        }