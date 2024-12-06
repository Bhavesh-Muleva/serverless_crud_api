import json
import os
import uuid
import boto3
from datetime import datetime
from typing import Dict, Any

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Validate required fields
        required_fields = ['title', 'description', 'status']
        if not all(field in body for field in required_fields):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Missing required fields: title, description, or status'
                })
            }
        
        # Validate status
        valid_statuses = ['pending', 'in-progress', 'completed']
        if body['status'] not in valid_statuses:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': f'Status must be one of: {", ".join(valid_statuses)}'
                })
            }

        # Create task item
        task = {
            'taskId': str(uuid.uuid4()),
            'title': body['title'],
            'description': body['description'],
            'status': body['status']
        }

        # Save to DynamoDB
        table.put_item(Item=task)

        return {
            'statusCode': 201,
            'body': json.dumps(task)
        }

    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal server error'
            })
        }