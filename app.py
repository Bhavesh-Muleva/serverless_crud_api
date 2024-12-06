#!/usr/bin/env python3
import aws_cdk as cdk
from serverless_crud_api.serverless_crud_api_stack import TaskApiStack

app = cdk.App()
TaskApiStack(app, "TaskApiStack")
app.synth()