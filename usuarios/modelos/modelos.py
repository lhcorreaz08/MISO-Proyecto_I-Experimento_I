import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

## Usuario model
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    username = db.Column(db.String(50), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    birthdate = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    address = db.Column(db.String(512), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    postalCode = db.Column(db.Integer, nullable=True)
    roleID = db.Column(db.Integer, nullable=True)
    bankAccountNumber = db.Column(db.Integer, nullable=True)
    bankAccountId= db.Column(db.Integer, nullable=True)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=db.func.now())


class UsuarioSchemaGet(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=[validate.Length(min=1, max=120)], load_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=1, max=50)], load_only=True)
    password = fields.Str(required=False, validate=[validate.Length(min=1, max=255)], load_only=True)
    name = fields.Str(required=False, validate=[validate.Length(min=1, max=500)], load_only=True)
    birthdate = fields.DateTime(required=False, load_only=True)
    address = fields.Str(required=False, validate=[validate.Length(min=1, max=512)], load_only=True)
    phone = fields.Str(required=False, validate=[validate.Length(min=1, max=20)], load_only=True)
    postalCode = fields.Int(required=False, load_only=True)
    roleID = fields.Int(required=False, load_only=True)
    bankAccountNumber = fields.Int(required=False, load_only=True)
    bankAccountId= fields.Int(required=False, load_only=True)
    createdAt = fields.DateTime(dump_only=True)
    
    class Meta:
        model = Usuario


class UsuarioSchemaPost(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=[validate.Length(min=1, max=120)], load_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=1, max=50)], load_only=True)
    password = fields.Str(required=True, validate=[validate.Length(min=1, max=255)], load_only=True)
    name = fields.Str(required=False, validate=[validate.Length(min=1, max=500)], load_only=True)
    birthdate = fields.DateTime(required=False, load_only=True)
    address = fields.Str(required=False, validate=[validate.Length(min=1, max=512)], load_only=True)
    phone = fields.Str(required=False, validate=[validate.Length(min=1, max=20)], load_only=True)
    postalCode = fields.Int(required=False, load_only=True)
    roleID = fields.Int(required=False, load_only=True)
    bankAccountNumber = fields.Int(required=False, load_only=True)
    bankAccountId= fields.Int(required=False, load_only=True)
    createdAt = fields.DateTime(dump_only=True)

    class Meta:
        model = Usuario




