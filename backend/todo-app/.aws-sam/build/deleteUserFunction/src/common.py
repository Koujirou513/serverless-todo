# common.py

def create_common_headers():
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,OPTIONS,PUT,POST,DELETE",
        "Access-Control-Allow-Headers": "Origin,Authorization,Accept,X-Requested-With,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Credentials": "true"
    }
