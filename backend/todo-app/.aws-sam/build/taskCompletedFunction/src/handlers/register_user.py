import json
import boto3
import hashlib
import os
import uuid
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

def lambda_handler(event, context):
    try:
        logger.info("Starting function")
        # リクエストボディの解析
        body = json.loads(event['body'])

        name = body['name']
        email = body['email']
        password = body['password']
        birthdate = body['birthdate']
        gender = body['gender']

        logger.info("Connecting to DynamoDB")

        # パスワードのハッシュ化
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # ユーザーIDの生成
        user_id = str(uuid.uuid4())

        logger.info("Processing data")

        # DynamoDBへの項目の挿入
        table.put_item(
            Item={
                'PK': f'USER#{user_id}',
                'SK': f'USER#{user_id}',
                'Name': name,
                'Email': email,
                'Password': hashed_password,
                'Birthdate': birthdate,
                'Gender': gender
            }
        )

        # レスポンスの生成
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User registered successfully', 'userId': user_id})
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to register user', 'error': str(e)})
        }