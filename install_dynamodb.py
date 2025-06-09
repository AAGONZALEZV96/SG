import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil

def download_dynamodb_local():
    """Download and setup DynamoDB Local manually"""
    
    print("🔄 Descargando DynamoDB Local...")
    
    # Create .dynamodb directory
    dynamodb_dir = os.path.join(os.getcwd(), '.dynamodb')
    if not os.path.exists(dynamodb_dir):
        os.makedirs(dynamodb_dir)
    
    # Download URL
    url = "https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.zip"
    zip_path = os.path.join(dynamodb_dir, "dynamodb_local.zip")
    
    try:
        urllib.request.urlretrieve(url, zip_path)
        print("✅ Descarga completada")
        
        # Extract zip
        print("📦 Extrayendo archivos...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dynamodb_dir)
        
        # Remove zip file
        os.remove(zip_path)
        
        print("✅ DynamoDB Local instalado correctamente")
        print(f"📁 Ubicación: {dynamodb_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al descargar DynamoDB Local: {str(e)}")
        return False

def start_dynamodb_local():
    """Start DynamoDB Local"""
    dynamodb_dir = os.path.join(os.getcwd(), '.dynamodb')
    jar_path = os.path.join(dynamodb_dir, 'DynamoDBLocal.jar')
    
    if not os.path.exists(jar_path):
        print("❌ DynamoDB Local no encontrado. Ejecutando instalación...")
        if not download_dynamodb_local():
            return False
    
    print("🚀 Iniciando DynamoDB Local...")
    
    try:
        # Start DynamoDB Local
        cmd = [
            'java', '-Djava.library.path=./DynamoDBLocal_lib',
            '-jar', 'DynamoDBLocal.jar',
            '-sharedDb', '-port', '8000'
        ]
        
        subprocess.Popen(cmd, cwd=dynamodb_dir)
        print("✅ DynamoDB Local iniciado en puerto 8000")
        print("🌐 Admin UI: http://localhost:8000/shell")
        return True
        
    except Exception as e:
        print(f"❌ Error al iniciar DynamoDB Local: {str(e)}")
        print("💡 Asegúrate de tener Java instalado")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        start_dynamodb_local()
    else:
        download_dynamodb_local()
