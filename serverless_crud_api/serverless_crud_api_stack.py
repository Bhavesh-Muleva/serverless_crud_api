from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    RemovalPolicy
)
from constructs import Construct
import os

class TaskApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB table
        tasks_table = dynamodb.Table(
            self, "TasksTable",
            partition_key=dynamodb.Attribute(
                name="taskId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # For development only
        )

        # Create Lambda functions
        lambda_path = os.path.join(os.path.dirname(__file__), "lambda")

        create_task_fn = _lambda.Function(
            self, "CreateTaskFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="create_task.handler",
            code=_lambda.Code.from_asset(lambda_path),
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )

        get_task_fn = _lambda.Function(
            self, "GetTaskFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="get_task.handler",
            code=_lambda.Code.from_asset(lambda_path),
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )

        update_task_fn = _lambda.Function(
            self, "UpdateTaskFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="update_task.handler",
            code=_lambda.Code.from_asset(lambda_path),
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )

        delete_task_fn = _lambda.Function(
            self, "DeleteTaskFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="delete_task.handler",
            code=_lambda.Code.from_asset(lambda_path),
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )

        # Grant DynamoDB permissions
        tasks_table.grant_write_data(create_task_fn)
        tasks_table.grant_read_data(get_task_fn)
        tasks_table.grant_write_data(update_task_fn)
        tasks_table.grant_write_data(delete_task_fn)

        # Create API Gateway
        api = apigateway.RestApi(
            self, "TasksApi",
            rest_api_name="Tasks Service",
            description="This is the Tasks API"
        )

        tasks = api.root.add_resource("tasks")
        task = tasks.add_resource("{taskId}")

        # Add methods to API Gateway
        tasks.add_method(
            "POST", 
            apigateway.LambdaIntegration(create_task_fn)
        )
        task.add_method(
            "GET", 
            apigateway.LambdaIntegration(get_task_fn)
        )
        task.add_method(
            "PUT", 
            apigateway.LambdaIntegration(update_task_fn)
        )
        task.add_method(
            "DELETE", 
            apigateway.LambdaIntegration(delete_task_fn)
        )