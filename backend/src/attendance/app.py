# src/attendance/app.py
import uuid
from datetime import datetime
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from mangum import Mangum

# Importa la configuración de la base de datos
from src.common.db_config import dynamodb_client, ATTENDANCE_TABLE

app = Flask(__name__)
CORS(app)

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

@app.errorhandler(404)
def resource_not_found(e):
    print(f"ERROR 404: Ruta no encontrada en Attendance API.")
    print(f"ERROR 404: request.path: {request.path}")
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == '__main__':
    app.run(debug=True)

handler = Mangum(app)