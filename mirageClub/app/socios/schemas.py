from app import db, ma
from marshmallow import fields


class SocioSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Id_persona = fields.Integer()
    Fingreso = fields.Date()
    Activo = fields.Boolean()


socio_schema = SocioSchema()
