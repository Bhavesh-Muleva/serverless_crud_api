import os
import boto3
import json
from typing import Dict, Any

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Extract taskId from path parameters
        task_id = event['pathParameters']['taskId']
         # Query DynamoDB for the task
        response = table.get_item(Key={'taskId': task_id})
        # Return successful response with task data
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    except Exception as e:
        # Return error response if anything goes wrong
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
