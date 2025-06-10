# Usa una imagen base oficial de AWS Lambda para Python 3.11
# Esta imagen ya incluye el Runtime Interface Client (RIC)
FROM public.ecr.aws/lambda/python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /var/task

# Copia tu archivo de requisitos de Python y el package.json (para npm install de plugins)
# Aunque aquí no se usará npm install para la Lambda, es una buena práctica para el contexto del proyecto
COPY requirements.txt ./
# COPY package.json ./ # No es necesario para el runtime de Python Lambda

# Instala las dependencias de Python usando pip (dentro del entorno de la imagen Lambda)
# El comando RUN pip install -r requirements.txt ya se encarga de instalar Flask, Flask-Cors, boto3
# --no-cache-dir para reducir el tamaño de la imagen final
# --upgrade pip para asegurar que pip esté actualizado
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia tu código de aplicación
# app.py contiene tu lógica Flask
# wsgi_handler.py es el manejador que conecta Lambda con Flask
COPY app.py ./
COPY wsgi_handler.py ./

# Define el comando que Lambda ejecutará cuando se invoque la función
# Esto le dice al RIC (Runtime Interface Client) dónde encontrar tu manejador.
# wsgi_handler.handler es el manejador que serverless-wsgi te proporciona.
CMD [ "wsgi_handler.handler" ]