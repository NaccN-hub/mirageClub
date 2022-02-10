from app import db, ma
from marshmallow import fields


class PersonaSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Nombre = fields.String()
    Dni = fields.String()
    Direccion = fields.String()
    Fnacimiento = fields.Date()
    Sexo = fields.Boolean()
    Telefono = fields.String()
    Email = fields.String()
    Activo = fields.Boolean()


class PersonaSchemaSimple (ma.Schema):
    Nombre = fields.String()
    Dni = fields.String()
    Fnacimiento = fields.Date()
    Sexo = fields.Boolean()
    Activo = fields.Boolean()


persona_schema = PersonaSchema()
persona_simple_schema = PersonaSchemaSimple()
