# Empezar corriendo una imagen de python 
FROM python:3.8-alpine

# Copiar requerimientos para ejecutar el programa
COPY ./requirements.txt /appusuarios/requirements.txt

EXPOSE 80

# Cambiar de directorio de trabajo a donde esta el ejectuable del API
WORKDIR /appusuarios

# Instalar requerimientos de la app
RUN pip install -r requirements.txt

# Copiar el contenido del directorio actual en la imagen de docker
COPY . /appusuarios

COPY entrypoint.sh /appusuarios/

RUN chmod +x /appusuarios/entrypoint.sh

RUN /appusuarios/entrypoint.sh

# Archivo principal donde corre el API
CMD [ "python", "app.py" ]