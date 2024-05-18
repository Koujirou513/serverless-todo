import json
import os
import boto3
import hashlib

table_name = os.environ.get('TABLE_NAME')
dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')

# DynamoDBリソースの初期化
if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(table_name)

def loginHandler(event, context):    
    try:
        #リクエストボディの解析
        body = json.loads(event['body'])
        
        #デバッグ用
        print(f"Request body: {body}")
        
        email = body['email']
        password = body['password']
        
        #パスワードのハッシュ化
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"Hashed password: {hashed_password}")
        
        #DynamoDBから特定のメールアドレスに基づくアイテムを取得
        response = table.scan(
            FilterExpression="Email = :email",
            ExpressionAttributeValues={
                ':email': email
            }
        )
        print(f"DynamoDB response: {response}") #デバッグ用
        
        items = response.get('Items', [])
        print(f"Items: {items}")  #デバッグ用
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
        
        item = items[0] # メールアドレスは一意であると仮定
        
        #パスワードの検証
        if item['Password'] != hashed_password:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Invalid password'})
            }
        
        #ユーザーIDを返す
        user_id = item['PK']
        
        return {
            'statusCode': 200,
            'body': json.dumps({'userId': user_id})
        }
        
    except Exception as e:
        print(f"Error retrieving user data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Faild to fetch user data', 'error': str(e)})
        }
        