from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
from os import getenv
from modelos import db
from vistas import Health, VistaSignIn, Ping

def set_env():
    load_dotenv()
    global DATABASE_URL
    DATABASE_URL = getenv("DATABASE_URL")
    global JWT_SECRET_KEY
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    
set_env()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaSignIn, '/users')
api.add_resource(Ping, '/users/ping')
api.add_resource(Health, '/')



jwt = JWTManager(app)

def unauthorized_response():
    return ("Usuario o Token no válido", 401)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return unauthorized_response()
@jwt.invalid_token_loader
def invalid_callback(callback):
    return unauthorized_response()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
