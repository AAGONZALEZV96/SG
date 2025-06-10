# src/auth/app.py
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

# Importa la configuración de la base de datos
from src.common.db_config import dynamodb_client, USERS_TABLE

app = Flask(__name__)
CORS(app)

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

@app.errorhandler(404)
def resource_not_found(e):
    print(f"ERROR 404: Ruta no encontrada en Auth API.")
    print(f"ERROR 404: request.path: {request.path}")
    return make_response(jsonify(error='Not found!'), 404)