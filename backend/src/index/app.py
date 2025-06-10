# backend/src/index/app.py (¡Elimina la función handler anterior!)

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from mangum import Mangum

# Importa la configuración de la base de datos (si esta API la necesita)
# from src.common.db_config import dynamodb_client # Descomenta si necesitas acceder a DynamoDB aquí

app = Flask(__name__)
CORS(app)

@app.route('/') # Esta será la ruta raíz para esta función Lambda
def index():
    print(f"DEBUG: Accediendo a la ruta raíz de Index API.")
    print(f"DEBUG: request.path: {request.path}")
    return jsonify({"mensaje": "¡Index API funcionando con Flask y Serverless!"})

@app.errorhandler(404)
def resource_not_found(e):
    print(f"ERROR 404: Ruta no encontrada en Index API.")
    print(f"ERROR 404: request.path: {request.path}")
    return make_response(jsonify(error='Not found!'), 404)

# --- ¡NUEVO! Añade este bloque al final de CADA app.py modularizado ---
# Esto es para que Flask pueda ejecutarse directamente en desarrollo si lo necesitas,
# pero no se ejecutará cuando sea invocado como Lambda.
if __name__ == '__main__':
    app.run(debug=True)

handler = Mangum(app)