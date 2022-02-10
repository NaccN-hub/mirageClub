from app import db, ma
from marshmallow import fields


class sociosActividadSchema(ma.Schema):
    Id = fields.Integer(dump_only=True)
    IdActividad = fields.Integer()
    IdSocio = fields.Integer()
    FechaInicio = fields.Date()
    Activo = fields.Boolean()


class sociosActividadSchemaSimple(ma.Schema):
    IdActividad = fields.String()
    IdSocio = fields.Integer()
    FechaInicio = fields.Date()
    Activo = fields.Boolean()


sociosActividad_schema = sociosActividadSchema()
sociosActividad_schema_simple = sociosActividadSchemaSimple()
