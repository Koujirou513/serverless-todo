import json
import os
import boto3
import hashlib

table_name = os.environ.get('TABLE_NAME')
dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')

if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(table_name)

def loginHandler(event, context):
    headers = create_common_headers()

    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS,PUT,POST,DELETE",
                "Access-Control-Allow-Headers": "Content-Type,",
            },
            'body': json.dumps('CORS preflight check')
        }

    try:
        body = json.loads(event['body'])
        email = body['email']
        password = body['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        response = table.scan(
            FilterExpression="Email = :email",
            ExpressionAttributeValues={':email': email}
        )

        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }

        item = items[0]
        if item['Password'] != hashed_password:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Invalid password'})
            }

        user_id = item['PK']
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS,PUT,POST,DELETE",
                "Access-Control-Allow-Headers": "Content-Type,",
            },
            'body': json.dumps({'userId': user_id})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to fetch user data', 'error': str(e)})
        }

        