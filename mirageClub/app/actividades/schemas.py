from app import db, ma
from marshmallow import fields


class ActividadSchema (ma.Schema):
    Id= fields.Integer(dump_only = True)
    Nombre= fields.String()
    Valor= fields.Float()
    Descripcion= fields.String()
    Activo= fields.Boolean()
    
class ActividadSchemaPublic (ma.Schema):
    Nombre= fields.String()
    Valor= fields.Float()
    Descripcion= fields.String()
    Activo= fields.Boolean()
    

actividad_schema = ActividadSchema()
actividad_public_schema = ActividadSchemaPublic