import json
import os
import json

from google.cloud import pubsub_v1

# Se leen las variables de entorno especificadas
#projec_id = os.environ.get('PROJECT_ID', '')
#tema_publicacion = os.environ.get('TOPIC', '')

project_id = "cloud-native-15"
tema_publicacion = "users_verification"

# Instancia del cliente de comunicación  Pub/Sub
publisher = pubsub_v1.PublisherClient()

class Publisher():

    def peticion_verificacion(data):
        """Definición de la función para realizar una llamada de auxilio. 
        La función realiza la publicación de un mensaje en el tema especificado
        
        Args:
            request (flask.Request): Objeto con la información de la petición.
        Returns:
            Información de la tarea creada
        """
        # Construye el nombre del tema a la que se realizará la publicación del mensaje
        topic_path = publisher.topic_path(project_id, tema_publicacion)
        # Construcción del mensaje que se enviará
        # data = json.dumps(data)
        message =  "Nueva verificación completada"
        attributes  = {
            'id': str(data["id"]),
            'email': str(data["email"]),
            'ruv': str(data["ruv"]),
            'score': str(data["score"]),
            'createdAt': str(data["date"]),
            'isVerified': str(data["isVerified"]),
            "usuario": str(data["usuario"]),
            "fullName": str(data["fullName"]),
            "phone": str(data["phone"]),
            "dni": str(data["dni"])
        }
        message_bytes = message.encode()
        # Se realiza la publicación del mensaje en el topico
        try:
            publish_future = publisher.publish(topic_path, message_bytes, **attributes )
            publish_future.result()  # Verify the publish succeeded
            return 'Se recibe la solicitud de verificación de usuario'
        except Exception as e:
            print('Error al momento de publicar')
            print(e)
            return e
