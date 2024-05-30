import json
import boto3
import os
import logging
from datetime import datetime
from decimal import Decimal


logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = os.environ.get('TABLE_NAME')
dynamodb_endpoint_url = os.environ.get('DYNAMODB_ENDPOINT_URL')

# DynamoDBリソースの初期化
if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(table_name)

def get_life_expectancy(gender):
    # 性別に基づく平均寿命を返す
    if gender.lower() == 'male':
        return 81 # 男性の平均寿命
    elif gender.lower() == 'female':
        return 87 # 女性の平均寿命
    else:
        return 84 # その他の場合の平均寿命
    
def calculate_remaining_life(birthdate_str, gender):
    # 生年月日と性別から残りの人生期間を計算
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
    today = datetime.now()
    age_days = (today - birthdate).days
    life_expectancy_days = get_life_expectancy(gender) * 365
    
    remaining_days = life_expectancy_days - age_days
    remaining_years = remaining_days // 365
    remaining_days %= 365
    
    return remaining_years, remaining_days

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
    
def calculate_todo_progress(todo, tasks):
    total_tasks = len(tasks)
    completed_tasks = sum(task['Completed'] for task in tasks)
    
    progress_percentage = (completed_tasks/ total_tasks * 100) if total_tasks > 0 else 0
    target_date = datetime.strptime(todo['TargetDate'], '%Y-%m-%d')
    remaining_days = (target_date - datetime.now()).days
    
    return {
        'Id': todo['SK'], 
        'Title': todo['Title'],
        'RemainingDays': remaining_days,
        'Progress': progress_percentage
    }


def get_user_info_handler(event, context):
    try:
        logger.info("Starting function")
        
        user_id = event['queryStringParameters']['userId']
        
        response = table.get_item(
            Key={
                'PK': user_id,
                'SK': user_id
            }
        )
        user = response.get('Item', {})
        
        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
            
        birthdate = user.get('Birthdate')
        gender = user.get('Gender')
        
        if not birthdate or not gender:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Birthdate and Gender are required'})
            }
        
        # 残りの人生期間を計算    
        remaining_years, remaining_days = calculate_remaining_life(birthdate, gender)
        
        # ToDo情報を取得
        response = table.query(
            KeyConditionExpression="PK = :pk and begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ':pk': user_id,
                ':sk_prefix': 'TODO#'
            }
        )
        todos = response.get('Items', [])
        
        todo_infos = [] 
        for todo in todos:
            todo_id = todo['SK']
            # 各ToDoのタスク情報を取得
            tasks_response = table.query(
                KeyConditionExpression="PK = :pk and begins_with(SK, :sk_prefix)",
                ExpressionAttributeValues={
                    ':pk': user_id,
                    ':sk_prefix': f'{todo_id}#TASK#'
                }
            )
            tasks = tasks_response.get('Items', [])
            
            #ToDoごとの進捗と残り日数を計算
            todo_info = calculate_todo_progress(todo, tasks)
            todo_infos.append(todo_info)
        
        result = {
            'user': {
                'RemainingLife': {
                    'Years': remaining_years,
                    'Days': remaining_days
                }
            },
            'todos': todo_infos
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(result, cls=DecimalEncoder)
        }
        
    except Exception as e:
        logger.error(f'Error retrieving data: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to fetch user data', 'error': str(e)})
        }
