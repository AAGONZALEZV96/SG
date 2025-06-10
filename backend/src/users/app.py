# src/users/app.py
import uuid
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from mangum import Mangum

# Importa la configuración de la base de datos desde el módulo común
from src.common.db_config import dynamodb_client, USERS_TABLE

# Crea una instancia de Flask para esta micro-aplicación
app = Flask(__name__)
CORS(app) # Habilita CORS para esta micro-aplicación

# Users endpoints
@app.route('/users/<string:user_id>')
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

@app.route('/users', methods=['GET'])
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

# Manejador de errores 404 (puedes dejarlo aquí o tener uno centralizado)
@app.errorhandler(404)
def resource_not_found(e):
    print(f"ERROR 404: Ruta no encontrada en Users API.")
    print(f"ERROR 404: request.path: {request.path}")
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == '__main__':
    app.run(debug=True)

handler = Mangum(app)