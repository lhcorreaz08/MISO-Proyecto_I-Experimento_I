import json
from unittest import TestCase
from flask_jwt_extended import create_access_token
import datetime

from faker import Faker
from faker.generator import random

from app import app, db

class TestPublicacion(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        db.session.begin_nested()
        self.user_id = self.data_factory.random_number(digits=2)
        self.token = create_access_token(identity=self.user_id)

    
    def tearDown(self):
        db.session.rollback()


    def test_crear_usuario(self):
        nueva_usuario = {
            "username": self.data_factory.text(8),
            "password": self.data_factory.text(8),
            "email": self.data_factory.email()
        }

        endpoint_usuario="/users"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
        print(respuesta_al_crear_usuario)
        user_id_nueva_oferta = respuesta_al_crear_usuario["id"]

        self.assertEqual(solicitud_nuevo_usuario.status_code, 201)



    def test_crear_usuario_sin_parametros(self):
        nueva_usuario = {
            "username": self.data_factory.text(8),
            "password": self.data_factory.text(8)
        }

        endpoint_usuario="/users"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
        print(respuesta_al_crear_usuario)

        self.assertEqual(solicitud_nuevo_usuario.status_code, 400)



    def test_crear_usuario_creado_previamente(self):
        nueva_usuario = {
            "username": self.data_factory.text(8),
            "password": self.data_factory.text(8),
            "email": self.data_factory.email()
        }

        endpoint_usuario="/users"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        solicitud_nuevo_usuario2 = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario),
                                                   headers=headers)
        respuesta_al_crear_usuario2 = json.loads(solicitud_nuevo_usuario.get_data())
        
        print(respuesta_al_crear_usuario)
        print(respuesta_al_crear_usuario2)

        self.assertEqual(solicitud_nuevo_usuario.status_code, 201)
        self.assertEqual(solicitud_nuevo_usuario2.status_code, 412)


    def test_login_sin_parametros_auth(self):
        nueva_usuario = {
            "username": self.data_factory.text(8)
        }

        endpoint_usuario="/users/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
        print(respuesta_al_crear_usuario)

        self.assertEqual(solicitud_nuevo_usuario.status_code, 400)


    def test_login_password_incorrecto_auth(self):

        username1 = self.data_factory.text(8)
        password1 = self.data_factory.text(6)
        password2 = self.data_factory.text(10)

        nueva_usuario1 = {
            "username": username1,
            "password": password1,
            "email": self.data_factory.email()
        }

        nueva_usuario2 = {
            "username": username1,
            "password": password2
        }


        endpoint_usuario="/users"    
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario1),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
        print(respuesta_al_crear_usuario)

        self.assertEqual(solicitud_nuevo_usuario.status_code, 201)


        endpoint_usuario="/users/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario1),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        solicitud_nuevo_usuario2 = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario2),
                                                   headers=headers)
        respuesta_al_crear_usuario2 = json.loads(solicitud_nuevo_usuario.get_data())
        
        print(respuesta_al_crear_usuario)
        print(respuesta_al_crear_usuario2)

        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)
        self.assertEqual(solicitud_nuevo_usuario2.status_code, 404)

    def test_login(self):

        username1 = self.data_factory.text(8)
        password1 = self.data_factory.text(6)

        nueva_usuario1 = {
            "username": username1,
            "password": password1,
            "email": self.data_factory.email()
        }

        endpoint_usuario="/users"    
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario1),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
        print(respuesta_al_crear_usuario)

        self.assertEqual(solicitud_nuevo_usuario.status_code, 201)


        endpoint_usuario="/users/auth"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.post(endpoint_usuario,
                                                   data=json.dumps(nueva_usuario1),
                                                   headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

       
        print(respuesta_al_crear_usuario)
        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)

    
    def test_pong(self):

        endpoint_usuario="/users/ping"    
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_usuario = self.client.get(endpoint_usuario, headers=headers)
        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())
        print(respuesta_al_crear_usuario)

        self.assertEqual(solicitud_nuevo_usuario.status_code, 200)



