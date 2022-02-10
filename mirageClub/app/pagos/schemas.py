from app import db, ma 
from marshmallow import fields

class PagoSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Fecha = fields.Date()
    Id_deuda = fields.Integer()
    Monto = fields.Integer()
    Descripcion = fields.String()
    Activo = fields.Boolean()
    Cerrado = fields.Boolean()
    Momento_carga = fields.Date()

pago_schema = PagoSchema()