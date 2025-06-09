import boto3
import json
import os
from datetime import datetime, timedelta
import uuid

# Configure DynamoDB client for local development
dynamodb = boto3.resource(
    'dynamodb',
    region_name='localhost',
    endpoint_url='http://localhost:8000',
    aws_access_key_id='fake',
    aws_secret_access_key='fake'
)

def seed_users():
    """Seed users table with initial data"""
    table = dynamodb.Table('users-table-dev')
    
    users = [
        {
            'userId': 'admin-1',
            'name': 'Administrador Sistema',
            'email': 'admin@sistema.com',
            'role': 'admin',
            'phone': '123456789'
        },
        {
            'userId': 'teacher-1',
            'name': 'María García',
            'email': 'teacher@sistema.com',
            'role': 'teacher',
            'phone': '987654321'
        },
        {
            'userId': 'student-1',
            'name': 'Carlos López',
            'email': 'student@sistema.com',
            'role': 'student',
            'phone': '456789123'
        },
        {
            'userId': 'student-2',
            'name': 'Ana Rodríguez',
            'email': 'ana@estudiante.com',
            'role': 'student',
            'phone': '789123456'
        },
        {
            'userId': 'student-3',
            'name': 'Luis Martínez',
            'email': 'luis@estudiante.com',
            'role': 'student',
            'phone': '321654987'
        }
    ]
    
    for user in users:
        table.put_item(Item=user)
        print(f"✅ Usuario creado: {user['name']} ({user['role']})")

def seed_attendance():
    """Seed attendance table with sample data"""
    table = dynamodb.Table('attendance-table-dev')
    
    students = ['student-1', 'student-2', 'student-3']
    student_names = ['Carlos López', 'Ana Rodríguez', 'Luis Martínez']
    
    # Generate attendance for last 30 days
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        current_date = base_date + timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        
        for j, student_id in enumerate(students):
            # 90% attendance rate
            present = True if (i + j) % 10 != 0 else False
            
            attendance = {
                'id': str(uuid.uuid4()),
                'studentId': student_id,
                'studentName': student_names[j],
                'classId': 'class-1',
                'className': 'Matemáticas Básicas',
                'date': date_str,
                'present': present
            }
            
            table.put_item(Item=attendance)
    
    print(f"✅ Asistencias creadas para los últimos 30 días")

def seed_grades():
    """Seed grades table with sample data"""
    table = dynamodb.Table('grades-table-dev')
    
    students = [
        {'id': 'student-1', 'name': 'Carlos López'},
        {'id': 'student-2', 'name': 'Ana Rodríguez'},
        {'id': 'student-3', 'name': 'Luis Martínez'}
    ]
    
    subjects = ['Matemáticas', 'Ciencias', 'Historia', 'Literatura', 'Inglés']
    comments = ['Excelente trabajo', 'Muy bien', 'Buen esfuerzo', 'Mejorando', 'Necesita práctica']
    
    base_date = datetime.now() - timedelta(days=60)
    
    for student in students:
        for i, subject in enumerate(subjects):
            # Generate 3-5 grades per subject per student
            num_grades = 3 + (hash(student['id'] + subject) % 3)
            
            for j in range(num_grades):
                grade_date = base_date + timedelta(days=i*10 + j*3)
                
                # Generate realistic grades (6.0 - 10.0)
                base_grade = 7.0 + (hash(student['id'] + subject + str(j)) % 30) / 10
                grade = round(min(10.0, max(6.0, base_grade)), 1)
                
                grade_record = {
                    'id': str(uuid.uuid4()),
                    'studentId': student['id'],
                    'studentName': student['name'],
                    'subject': subject,
                    'grade': grade,
                    'comment': comments[j % len(comments)],
                    'date': grade_date.strftime('%Y-%m-%d')
                }
                
                table.put_item(Item=grade_record)
    
    print(f"✅ Calificaciones creadas para todos los estudiantes")

def main():
    """Main function to seed all tables"""
    print("🌱 Iniciando proceso de seed de datos...")
    
    try:
        seed_users()
        seed_attendance()
        seed_grades()
        print("\n🎉 ¡Proceso de seed completado exitosamente!")
        print("\n📋 Credenciales de acceso:")
        print("👑 Admin: admin@sistema.com / admin123")
        print("👩‍🏫 Teacher: teacher@sistema.com / teacher123") 
        print("🎓 Student: student@sistema.com / student123")
        
    except Exception as e:
        print(f"❌ Error durante el seed: {str(e)}")

if __name__ == '__main__':
    main()
