# src/common/wsgi_handler.py
# Este es un manejador WSGI genérico para usar con serverless-wsgi

import sys
import os

# Añade el directorio padre al PYTHONPATH para que Python encuentre los módulos
# como 'src.common.db_config' o 'src.users.app'.
# Dependiendo de cómo se empaquete, puede que necesites ajustar esto.
# serverless-wsgi a menudo gestiona esto.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from serverless_wsgi import handle_request


# La instancia de la aplicación Flask se pasará a esta función
# a través de la configuración del serverless.yml para cada Lambda.
# Por ejemplo, para users: wsgi: app: src.users.app.app

def handler(event, context):
    """
    Este es el handler principal para AWS Lambda.
    Utiliza serverless_wsgi para procesar la solicitud.
    """
    # serverless-wsgi espera que 'app' sea una referencia directa al objeto Flask
    # esto se pasa en la configuración del serverless.yml: wsgi.app
    return handle_request(event['app'], event, context)

# Nota: No hay un if __name__ == '__main__': aquí, ya que este es un handler de Lambda.