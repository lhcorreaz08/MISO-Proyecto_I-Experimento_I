import random
import string
import requests
import hashlib
import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import db, Usuario, UsuarioSchema, UsuarioSchemaGet, UsuarioSchemaPost, UsuarioSchemaPostAuth, IsVerified
from pubservice import Publisher
from hashlib import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from datetime import timedelta
import os
from google.cloud import tasks_v2
import json

# Se leen las variables de entorno especificadas
location_id = os.environ.get('LOCATION_ID', '')
secret_token = os.environ.get('SECRET_TOKEN', '')
projec_id = os.environ.get('PROJECT_ID', '')
queue_id = os.environ.get('QUEUE_ID', '')
url_function = os.environ.get('URL_FUNCTION', '')

client = tasks_v2.CloudTasksClient()

usuario_schema = UsuarioSchema()
usuario_schema_get = UsuarioSchemaGet()
usuario_schema_post = UsuarioSchemaPost() 
usuario_schema_postauth = UsuarioSchemaPostAuth()

class VistaTest(Resource):
    @jwt_required()
    def post(self):
        return {"Hola": "Mundo"}

class VistaSignIn(Resource):

    def post(self):
        try:    
            if request.json["username"] is None or request.json["email"] is None or request.json["password"] is None:
                return {'message': 'Missing fields'}, 400
            requestedUser = Usuario.query.filter(Usuario.username == request.json["username"]).first()
            requestedEmail = Usuario.query.filter(Usuario.email == request.json["email"]).first()
            if requestedUser or requestedEmail:
                return {'message': 'User o email already exist'} , 412 
            else:
                username1 = request.json.get("username", None)
                password1 = request.json.get("password", None)
                saltValue = get_random_string(5)
                # DROP TYPE public."isverified";
                nuevo_usuario = Usuario(username=request.json["username"],
                                                email=request.json["email"],
                                                password = generate_password_hash(request.json["password"]),
                                                dni=request.json.get("dni"),
                                                fullName=request.json.get("fullName"),
                                                phone=request.json.get("phone"),
                                                isVerified=IsVerified.POR_VERIFICAR,
                                                salt = saltValue,
                                                token=create_access_token(identity=username1, expires_delta=timedelta(minutes=10)),
                                                expireAt= datetime.now(timezone.utc) + timedelta(minutes=10),
                                                createdAt= datetime.now(timezone.utc)
                                                )

                db.session.add(nuevo_usuario)
                db.session.commit()
                user = {
                    "id": nuevo_usuario.id,
                    "username": nuevo_usuario.username,
                    "email": nuevo_usuario.email,
                    "dni": nuevo_usuario.dni,
                    "fullName": nuevo_usuario.fullName,
                    "phone": nuevo_usuario.phone
                }
                produce_verification(json.dumps(user).encode())
            return usuario_schema_post.dump(nuevo_usuario), 201   
        except TypeError:
            return {'message': 'Missing fields'}, 400
        except KeyError:
            return {'message': 'Missing fields'}, 400
    

class VistaAuthenticator(Resource):

    def post(self):
        try:        
            if request.json["username"] is None or request.json["password"] is None:
                return {'message': 'Missing fields'}, 400
            usuario = Usuario.query.filter(Usuario.username == request.json["username"]).first()
            db.session.commit()
            if usuario:
                if check_password_hash(usuario.password, request.json["password"]):
                    if usuario.isVerified == IsVerified.VERIFICADO:
                        token_de_acceso = create_access_token(identity=usuario.id, expires_delta=timedelta(minutes=10))
                        usuario.token = token_de_acceso
                        usuario.expireAt = datetime.now(timezone.utc) + timedelta(minutes=10)
                        db.session.commit()
                        return usuario_schema_postauth.dump(usuario), 200
                    else:
                        return {"message": "User NO_VERIFICADO or user POR_VERIFICAR"}, 401
                else:
                    return {"message": "Password invalid"}, 404
            else:
                return {"message": "User not exist"} , 404

        except TypeError:
            return {'message': 'Missing fields'}, 400
        except KeyError:
            return {'message': 'Missing fields'}, 400
        except ValidationError as err: 
            for e in err.messages:
                print(e)
            for item in err.messages.items():
                print(item)
                if item[1][0] == "Missing data for required field.":
                    return {'message': 'Missing fields'}, 400
            return f'{err.messages}' , 412 



class VistaUserInformation(Resource):  
    @jwt_required(True)
    def get(self):
        user_id = get_jwt_identity()
        if user_id is None: 
            return {'message': 'Invalid id 400'}, 400
        try:
            id = int(user_id)
            if  id <= 0:
                return {'message': 'Invalid id 400'}, 400
        except ValueError:
            return {'message': 'Invalid id 400'}, 400
        usuario = Usuario.query.filter(Usuario.id == id).first()
        if usuario is None: 
            return  {'message': 'User not found 401'}, 401
        if usuario.id != id:
            return {'message': 'Unauthorized 401'}, 401
        return usuario_schema_get.dump(usuario), 200


class VistaUserWebhook(Resource):  
    def post(self):
        # Validar respuesta única
        ruv = request.json["RUV"]
        score = request.json["score"]
        token = f"{secret_token}:{ruv}:{score}"
        sha_token = hashlib.sha256(token.encode()).hexdigest()
        if sha_token == request.json["verifyToken"]:
            user_id = request.json["userIdentifier"]
            id = int(user_id)
            usuario = Usuario.query.filter(Usuario.id == id).first()
            if usuario is None:
                return {'message': 'Invalid user'}, 400
            if score >= 80:
                stringVer = "VERIFICADO"
                usuario.isVerified = IsVerified.VERIFICADO
            else:
                stringVer = "NO_VERIFICADO"
                usuario.isVerified = IsVerified.NO_VERIFICADO
            db.session.commit()

            id_res = usuario.id
            email_res = usuario.email

            pub_data = {
                "id": str(id_res),
                "email": str(email_res),
                "ruv": request.json["RUV"],
                "score": request.json["score"],
                "date": request.json["createdAt"],
                "isVerified": stringVer,
                "usuario": str(usuario.username),
                "fullName": str(usuario.fullName or ''),
                "phone": str(usuario.phone or ''),
                "dni": str(usuario.dni or '')
            }

            Publisher.peticion_verificacion(pub_data)
            return 200
        return {'message': 'Invalid token'}, 400


class VistaManualVerification(Resource):  
    def post(self):
        email = request.json["email"]
        if email is None or email == '':
            return  {'message': 'Bad request body 400'}, 400
        usuario = Usuario.query.filter(Usuario.email == email).first()
        if usuario is None:
            return  {'message': 'User not found'}, 404
        if usuario.isVerified == IsVerified.VERIFICADO:
            return  {'message': 'User Already Verified'}, 409
        user = {
                    "id": usuario.id,
                    "username": usuario.username,
                    "email": usuario.email,
                    "dni": usuario.dni,
                    "fullName": usuario.fullName,
                    "phone": usuario.phone
                }
        produce_verification(json.dumps(user).encode())
        return  {'message': 'Request Submitted'}, 200

class Health(Resource):
    def get(self):
        return "pong", 200

def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # print random string
    return(result_str)

def produce_verification(user):
    print("Produce verification")
     # Construye el nombre de la cola a la que se realizará la conexión
    parent = client.queue_path(projec_id, location_id, queue_id)
    print (parent)
    task = {
        "http_request": {  # Determina el tipo de tareas, en este caso una petición HTTP.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url_function,  # Determina la URL completa a la que se realizará el consumo del servicio.
            "headers": {
                "Content-type": "application/json"
            },
            "body": user,
        }
    }
    # Se realiza la creación de la tarea en la cola
    response = client.create_task(request={"parent": parent, "task": task})
    print("Created task {}".format(response.name))

   
