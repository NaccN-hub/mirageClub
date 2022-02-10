from app import db, ma
from marshmallow import fields


class DeudaSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Id_socio = fields.Integer()
    Descripcion = fields.String()
    Mes = fields.Date()
    Importe = fields.Float()
    Abonada = fields.Boolean()


deuda_schema = DeudaSchema()
