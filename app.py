import os
import uuid
from datetime import datetime

import boto3
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# DynamoDB configuration
if os.environ.get('IS_OFFLINE'):
    # LocalStack usa un endpoint unificado para todos los servicios
    # Usamos LOCALSTACK_HOSTNAME que pasamos en serverless.yml
    localstack_endpoint = os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')
    localstack_url = f"http://{localstack_endpoint}:4566" # Puerto por defecto de LocalStack

    dynamodb_client = boto3.client(
        'dynamodb',
        region_name='us-east-1', # La región debe coincidir con tu provider en serverless.yml
        endpoint_url=localstack_url, # <--- ¡APUNTA A LOCALSTACK!
        aws_access_key_id='test', # Credenciales de prueba de LocalStack
        aws_secret_access_key='test' # Credenciales de prueba de LocalStack
    )
    dynamodb_resource = boto3.resource(
        'dynamodb',
        region_name='us-east-1', # La región debe coincidir con tu provider en serverless.yml
        endpoint_url=localstack_url, # <--- ¡APUNTA A LOCALSTACK!
        aws_access_key_id='test', # Credenciales de prueba de LocalStack
        aws_secret_access_key='test' # Credenciales de prueba de LocalStack
    )
else:
    # Esto sigue siendo para el despliegue en la nube real
    dynamodb_client = boto3.client('dynamodb')
    dynamodb_resource = boto3.resource('dynamodb')

# Table names
USERS_TABLE = os.environ.get('USERS_TABLE', 'users-table-dev')
ATTENDANCE_TABLE = os.environ.get('ATTENDANCE_TABLE', 'attendance-table-dev')
GRADES_TABLE = os.environ.get('GRADES_TABLE', 'grades-table-dev')

# --- Rutas de Flask ---
# ¡IMPORTANTE! Las rutas de Flask NO LLEVAN el prefijo '/dev' aquí,
# porque ya está especificado en serverless.yml (path: dev/{proxy+}).
# Flask verá '/users', '/auth/login', etc.

@app.route('/') # Esta ruta corresponderá a http://localhost:3000/dev
def index():
    # Líneas de depuración (puedes dejarlas para ver qué Flask ve)
    print(f"DEBUG: Accediendo a la ruta raíz de Flask.")
    print(f"DEBUG: request.path: {request.path}")
    print(f"DEBUG: request.full_path: {request.full_path}")
    print(f"DEBUG: request.base_url: {request.base_url}")
    print(f"DEBUG: request.url_root: {request.url_root}")
    return jsonify({"mensaje": "¡Todo está funcionando con Flask y Serverless!"})

# Users endpoints
@app.route('/users/<string:user_id>') # Esta ruta corresponderá a http://localhost:3000/dev/users/<ID>
def get_user(user_id):
    result = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S'),
        'email': item.get('email', {}).get('S', ''),
        'role': item.get('role', {}).get('S', 'student'),
        'phone': item.get('phone', {}).get('S', '')
    })

@app.route('/users', methods=['GET']) # Esta ruta corresponderá a http://localhost:3000/dev/users
def get_users():
    result = dynamodb_client.scan(TableName=USERS_TABLE)
    items = result.get('Items', [])
    
    users = []
    for item in items:
        users.append({
            'userId': item.get('userId').get('S'),
            'name': item.get('name').get('S'),
            'email': item.get('email', {}).get('S', ''),
            'role': item.get('role', {}).get('S', 'student'),
            'phone': item.get('phone', {}).get('S', '')
        })
    
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = data.get('userId') or str(uuid.uuid4())
    name = data.get('name')
    email = data.get('email')
    role = data.get('role', 'student')
    phone = data.get('phone', '')
    
    if not name or not email:
        return jsonify({'error': 'Please provide both "name" and "email"'}), 400

    item = {
        'userId': {'S': user_id},
        'name': {'S': name},
        'email': {'S': email},
        'role': {'S': role}
    }
    
    if phone:
        item['phone'] = {'S': phone}

    dynamodb_client.put_item(TableName=USERS_TABLE, Item=item)

    return jsonify({
        'userId': user_id,
        'name': name,
        'email': email,
        'role': role,
        'phone': phone
    })

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    
    # Build update expression
    update_expression = "SET "
    expression_values = {}
    expression_names = {}
    
    if 'name' in data:
        update_expression += "#n = :name, "
        expression_values[':name'] = {'S': data['name']}
        expression_names['#n'] = 'name'
    
    if 'email' in data:
        update_expression += "email = :email, "
        expression_values[':email'] = {'S': data['email']}
    
    if 'phone' in data:
        update_expression += "phone = :phone, "
        expression_values[':phone'] = {'S': data['phone']}
    
    if 'role' in data:
        update_expression += "#r = :role, "
        expression_values[':role'] = {'S': data['role']}
        expression_names['#r'] = 'role'
    
    # Remove trailing comma and space
    update_expression = update_expression.rstrip(', ')
    
    try:
        dynamodb_client.update_item(
            TableName=USERS_TABLE,
            Key={'userId': {'S': user_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names if expression_names else None
        )
        
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        dynamodb_client.delete_item(
            TableName=USERS_TABLE,
            Key={'userId': {'S': user_id}}
        )
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Authentication endpoint
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Mock authentication - replace with real authentication
    # For demo purposes, we'll check if user exists in database
    result = dynamodb_client.scan(
        TableName=USERS_TABLE,
        FilterExpression='email = :email',
        ExpressionAttributeValues={':email': {'S': email}}
    )
    
    items = result.get('Items', [])
    if not items:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    user = items[0]
    return jsonify({
        'userId': user.get('userId').get('S'),
        'name': user.get('name').get('S'),
        'email': user.get('email').get('S'),
        'role': user.get('role', {}).get('S', 'student'),
        'phone': user.get('phone', {}).get('S', '')
    })

# Attendance endpoints
@app.route('/attendance', methods=['GET'])
def get_attendance():
    student_id = request.args.get('studentId')
    date = request.args.get('date')
    
    if student_id and date:
        # Get attendance for specific student and date
        result = dynamodb_client.query(
            TableName=ATTENDANCE_TABLE,
            IndexName='StudentDateIndex',
            KeyConditionExpression='studentId = :studentId AND #date = :date',
            ExpressionAttributeValues={
                ':studentId': {'S': student_id},
                ':date': {'S': date}
            },
            ExpressionAttributeNames={'#date': 'date'}
        )
    elif student_id:
        # Get all attendance for specific student
        result = dynamodb_client.query(
            TableName=ATTENDANCE_TABLE,
            IndexName='StudentDateIndex',
            KeyConditionExpression='studentId = :studentId',
            ExpressionAttributeValues={':studentId': {'S': student_id}}
        )
    else:
        # Get all attendance records
        result = dynamodb_client.scan(TableName=ATTENDANCE_TABLE)
    
    items = result.get('Items', [])
    attendance_records = []
    
    for item in items:
        attendance_records.append({
            'id': item.get('id').get('S'),
            'studentId': item.get('studentId').get('S'),
            'studentName': item.get('studentName', {}).get('S', ''),
            'classId': item.get('classId', {}).get('S', ''),
            'className': item.get('className', {}).get('S', ''),
            'date': item.get('date').get('S'),
            'present': item.get('present').get('BOOL')
        })
    
    return jsonify(attendance_records)

@app.route('/attendance', methods=['POST'])
def create_attendance():
    data = request.json
    attendance_id = str(uuid.uuid4())
    
    required_fields = ['studentId', 'date', 'present']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    item = {
        'id': {'S': attendance_id},
        'studentId': {'S': data['studentId']},
        'date': {'S': data['date']},
        'present': {'BOOL': data['present']}
    }
    
    # Optional fields
    if 'studentName' in data:
        item['studentName'] = {'S': data['studentName']}
    if 'classId' in data:
        item['classId'] = {'S': data['classId']}
    if 'className' in data:
        item['className'] = {'S': data['className']}
    
    dynamodb_client.put_item(TableName=ATTENDANCE_TABLE, Item=item)
    
    return jsonify({
        'id': attendance_id,
        'studentId': data['studentId'],
        'date': data['date'],
        'present': data['present']
    })

# Grades endpoints
@app.route('/grades', methods=['GET'])
def get_grades():
    student_id = request.args.get('studentId')
    subject = request.args.get('subject')
    
    if student_id and subject:
        result = dynamodb_client.query(
            TableName=GRADES_TABLE,
            IndexName='StudentSubjectIndex',
            KeyConditionExpression='studentId = :studentId AND subject = :subject',
            ExpressionAttributeValues={
                ':studentId': {'S': student_id},
                ':subject': {'S': subject} # Corregido: usar variable 'subject'
            }
        )
    elif student_id:
        result = dynamodb_client.query(
            TableName=GRADES_TABLE,
            IndexName='StudentSubjectIndex',
            KeyConditionExpression='studentId = :studentId',
            ExpressionAttributeValues={':studentId': {'S': student_id}}
        )
    else:
        result = dynamodb_client.scan(TableName=GRADES_TABLE)
    
    items = result.get('Items', [])
    grades = []
    
    for item in items:
        grades.append({
            'id': item.get('id').get('S'),
            'studentId': item.get('studentId').get('S'),
            'studentName': item.get('studentName', {}).get('S', ''),
            'subject': item.get('subject').get('S'),
            'grade': float(item.get('grade').get('N')),
            'comment': item.get('comment', {}).get('S', ''),
            'date': item.get('date').get('S')
        })
    
    return jsonify(grades)

@app.route('/grades', methods=['POST'])
def create_grade():
    data = request.json
    grade_id = str(uuid.uuid4())
    
    required_fields = ['studentId', 'subject', 'grade']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    item = {
        'id': {'S': grade_id},
        'studentId': {'S': data['studentId']},
        'subject': {'S': data['subject']},
        'grade': {'N': str(data['grade'])},
        'date': {'S': data.get('date', datetime.now().isoformat())}
    }
    
    if 'studentName' in data:
        item['studentName'] = {'S': data['studentName']}
    if 'comment' in data:
        item['comment'] = {'S': data['comment']}
    
    dynamodb_client.put_item(TableName=GRADES_TABLE, Item=item)
    
    return jsonify({
        'id': grade_id,
        'studentId': data['studentId'],
        'subject': data['subject'],
        'grade': data['grade'],
        'date': item['date']['S']
    })

@app.errorhandler(404)
def resource_not_found(e):
    # Líneas de depuración (puedes dejarlas para ver qué Flask ve)
    print(f"ERROR 404: Ruta no encontrada.")
    print(f"ERROR 404: request.path: {request.path}")
    print(f"ERROR 404: request.full_path: {request.full_path}")
    print(f"ERROR 404: request.base_url: {request.base_url}")
    print(f"ERROR 404: request.url_root: {request.url_root}")
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == '__main__':
    app.run(debug=True)