# SERVICIO OFERTA
El microservicio de gestión de ofertas permite crear y consultar ofertas.

# EJECUCIÓN Y DESPLIEGUE LOCAL

Si lo solo desea ejecutar este microservicio por favor ubicarse en la carpeta oferta y utilizar los siguientes comandos


## Remueve todos los contenedores (forzado)
docker rm -f $(docker ps -aq)

## Bajar todos los contenedores e imagenes

docker-compose -f docker-compose.prod.yml down -v

## Construye la imagen 

docker-compose -f docker-compose.prod.yml up -d --build 

## Consideraciones por sistema operativo 

### MacOS
Estar seguro en usuarios MacOS de tener apagado AirPlay Receiver
(Go to System Preference --> Sharing --> uncheck off the AirPlay Receiver)

### WINDOWS
Estar seguro que los archivos docker-compose.prod.yml, Dockerfile.prod, entrypoint.prod.sh están  en LF (configuración de salto de línea en el editor de texto) para Linux 

### El end point del request es http://localhost:3000/

## Collection Cloud Native Grupo 15. 
[cloudnative.postman_collection.json](https://documenter.getpostman.com/view/20288420/2s935vkKak)
