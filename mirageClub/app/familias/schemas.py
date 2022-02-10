from app import db, ma
from marshmallow import fields

class FamiliaSchema(ma.Schema):
    Id = fields.Integer(dump_only = True)
    Id_persona = fields.Integer()
    Id_socio = fields.Integer()
    Fingreso = fields.Date()
    Activo = fields.Boolean()

class FamiliaSchemaSimple(ma.Schema):
    Id_persona = fields.Integer()
    Id_socio = fields.Integer()
    Fingreso = fields.Date()
    Activo = fields.Boolean()

Familia_schema = FamiliaSchema()
Familia_schema_simple = FamiliaSchemaSimple()