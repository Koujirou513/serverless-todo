import json
import boto3
import hashlib
import os
import uuid

# DynamoDBリソースの初期化
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    # リクエストボディの解析
    body = json.loads(event['body'])
    name = body['name']
    email = body['email']
    password = body['password']
    birthdate = body['birthdate']
    gender = body['gender']

    # パスワードのハッシュ化
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # ユーザーIDの生成
    user_id = str(uuid.uuid4())

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