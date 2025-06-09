import boto3
import os
import time

def create_tables():
    """Create DynamoDB tables manually if needed"""
    
    # Configure DynamoDB client for local development
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000',
        aws_access_key_id='fake',
        aws_secret_access_key='fake'
    )
    
    # Table configurations
    tables_config = [
        {
            'TableName': 'users-table-dev',
            'KeySchema': [
                {'AttributeName': 'userId', 'KeyType': 'HASH'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'userId', 'AttributeType': 'S'}
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': 'attendance-table-dev',
            'KeySchema': [
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'studentId', 'AttributeType': 'S'},
                {'AttributeName': 'date', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'StudentDateIndex',
                    'KeySchema': [
                        {'AttributeName': 'studentId', 'KeyType': 'HASH'},
                        {'AttributeName': 'date', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        },
        {
            'TableName': 'grades-table-dev',
            'KeySchema': [
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'studentId', 'AttributeType': 'S'},
                {'AttributeName': 'subject', 'AttributeType': 'S'}
            ],
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'StudentSubjectIndex',
                    'KeySchema': [
                        {'AttributeName': 'studentId', 'KeyType': 'HASH'},
                        {'AttributeName': 'subject', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        }
    ]
    
    created_tables = []
    
    for table_config in tables_config:
        table_name = table_config['TableName']
        
        try:
            # Check if table exists
            table = dynamodb.Table(table_name)
            table.load()
            print(f"✅ Tabla '{table_name}' ya existe")
            
        except dynamodb.meta.client.exceptions.ResourceNotFoundException:
            # Create table
            print(f"🔄 Creando tabla '{table_name}'...")
            
            table = dynamodb.create_table(**table_config)
            created_tables.append(table_name)
            
            # Wait for table to be created
            table.wait_until_exists()
            print(f"✅ Tabla '{table_name}' creada exitosamente")
            
        except Exception as e:
            print(f"❌ Error con tabla '{table_name}': {str(e)}")
    
    if created_tables:
        print(f"\n🎉 Tablas creadas: {', '.join(created_tables)}")
    else:
        print("\n📋 Todas las tablas ya existían")
    
    return True

if __name__ == '__main__':
    print("🗄️ Configurando tablas DynamoDB Local...")
    
    # Wait a moment for DynamoDB Local to be ready
    time.sleep(2)
    
    try:
        create_tables()
        print("\n✅ Configuración de tablas completada")
    except Exception as e:
        print(f"\n❌ Error en configuración: {str(e)}")
        print("💡 Asegúrate de que DynamoDB Local esté ejecutándose en puerto 8000")
