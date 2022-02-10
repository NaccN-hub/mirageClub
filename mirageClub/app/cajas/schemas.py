from app import db, ma
from marshmallow import fields


class IngresoSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Id_socio = fields.Integer()
    Fecha = fields.Date()
    Monto = fields.Integer()
    Descripcion = fields.String()
    Eliminado = fields.Boolean()
    Fcarga = fields.Date()


class EgresoSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Id_rubro = fields.Integer()
    Fecha = fields.Date()
    Importe = fields.Integer()
    Descripcion = fields.String()
    Fcarga = fields.Date()


class RubroSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Nombre = fields.String()
    Eliminado = fields.Boolean()


ingreso_schema = IngresoSchema()
egreso_schema = EgresoSchema()
rubro_schema = RubroSchema()
