# src/grades/app.py
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
import uuid

# Importa la configuración de la base de datos
from src.common.db_config import dynamodb_client, GRADES_TABLE

app = Flask(__name__)
CORS(app)

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
                ':subject': {'S': subject}
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
    print(f"ERROR 404: Ruta no encontrada en Grades API.")
    print(f"ERROR 404: request.path: {request.path}")
    return make_response(jsonify(error='Not found!'), 404)