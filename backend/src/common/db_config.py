# src/common/db_config.py
import os
import boto3

# DynamoDB configuration
if os.environ.get('IS_OFFLINE'):
    localstack_endpoint = os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')
    localstack_url = f"http://{localstack_endpoint}:4566"

    dynamodb_client = boto3.client(
        'dynamodb',
        region_name='us-east-1',
        endpoint_url=localstack_url,
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
    dynamodb_resource = boto3.resource(
        'dynamodb',
        region_name='us-east-1',
        endpoint_url=localstack_url,
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
else:
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_resource = boto3.resource('dynamodb')

# Table names
USERS_TABLE = os.environ.get('USERS_TABLE', 'users-table-dev')
ATTENDANCE_TABLE = os.environ.get('ATTENDANCE_TABLE', 'attendance-table-dev')
GRADES_TABLE = os.environ.get('GRADES_TABLE', 'grades-table-dev')

# Puedes devolverlos como un diccionario si prefieres, o usarlos directamente.
# Para simplicidad, los dejamos como variables globales que se importarán.