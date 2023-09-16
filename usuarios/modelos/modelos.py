import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


## Enumeration of possible states
class IsVerified(enum.Enum):
    VERIFICADO = "VERIFICADO"
    NO_VERIFICADO = "NO_VERIFICADO"
    POR_VERIFICAR = "POR_VERIFICAR"

## Usuario model
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255))
    dni = db.Column(db.String(100), nullable=True)
    fullName = db.Column(db.String(512), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    isVerified = db.Column(db.Enum(IsVerified))
    salt = db.Column(db.String(512))
    token = db.Column(db.String(512))
    expireAt = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    createdAt = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

## Serializer
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return f'{value.value}'

class UsuarioSchema(SQLAlchemyAutoSchema):
    isVerified = EnumADiccionario(attribute=("isVerified"))
    class Meta:
        model = Usuario
        load_instance = True


class UsuarioSchemaGet(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=1, max=50)], load_only=True, dump_only=True)
    email = fields.Str(required=True, validate=[validate.Length(min=1, max=120)], load_only=True, dump_only=True)
    password = fields.Str(required=True, validate=[validate.Length(min=1, max=255)], load_only=True)
    dni = fields.Str(required=False, validate=[validate.Length(min=1, max=100)], load_only=True, dump_only=True)
    fullName = fields.Str(required=False, validate=[validate.Length(min=1, max=512)], load_only=True, dump_only=True)
    phone = fields.Str(required=False, validate=[validate.Length(min=1, max=255)], load_only=True, dump_only=True)
    isVerified = EnumADiccionario(attribute=("isVerified"), required=True, validate=[validate.OneOf([item.value for item in IsVerified])])	
    salt = fields.Str(required=True, validate=[validate.Length(min=1, max=512)], load_only=True)
    token = fields.Str(required=True, validate=[validate.Length(min=1, max=512)], load_only=True)
    expireAt = fields.DateTime(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)

    class Meta:
        model = Usuario


class UsuarioSchemaPost(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=1, max=50)], load_only=True)
    email = fields.Str(required=True, validate=[validate.Length(min=1, max=120)], load_only=True)
    password = fields.Str(required=True, validate=[validate.Length(min=1, max=255)], load_only=True)
    dni = fields.Str(required=False, validate=[validate.Length(min=1, max=100)], load_only=True, dump_only=True)
    fullName = fields.Str(required=False, validate=[validate.Length(min=1, max=512)], load_only=True, dump_only=True)
    phone = fields.Str(required=False, validate=[validate.Length(min=1, max=255)], load_only=True, dump_only=True)
    isVerified = EnumADiccionario(attribute=("isVerified"), required=True, validate=[validate.OneOf([item.value for item in IsVerified])] , load_only=True)	
    salt = fields.Str(validate=[validate.Length(min=1, max=512)], load_only=True)
    token = fields.Str(validate=[validate.Length(min=1, max=512)], load_only=True)
    expireAt = fields.DateTime(load_only=True)
    createdAt = fields.DateTime(dump_only=True)

    class Meta:
        model = Usuario

class UsuarioSchemaPostAuth(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=1, max=50)], load_only=True)
    email = fields.Str(required=True, validate=[validate.Length(min=1, max=120)], load_only=True)
    password = fields.Str(required=True, validate=[validate.Length(min=1, max=255)], load_only=True)
    isVerified = EnumADiccionario(attribute=("isVerified"), required=True, validate=[validate.OneOf([item.value for item in IsVerified])] , load_only=True)
    salt = fields.Str(validate=[validate.Length(min=1, max=512)], load_only=True)
    token = fields.Str(validate=[validate.Length(min=1, max=512)], dump_only=True)
    expireAt = fields.DateTime(dump_only=True)
    createdAt = fields.DateTime(load_only=True)

    class Meta:
        model = Usuario



