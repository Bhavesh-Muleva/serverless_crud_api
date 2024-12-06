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
        # Delete the task from DynamoDB
        table.delete_item(Key={'taskId': task_id})
        # Return successful response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Task deleted successfully'})
        }
    except Exception as e:
        # Return error response if anything goes wrong
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
