from app import db, ma
from marshmallow import fields


class UsuarioSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Nombre = fields.String()
    Contrasenia = fields.String()
    Id_socio = fields.Integer()
    Id_tipousuario = fields.Integer()
    Fcarga = fields.Date()


class TipousuarioSchema (ma.Schema):
    Id = fields.Integer(dump_only=True)
    Nombre = fields.String()
    Descripcion = fields.String()

usuario_schema = UsuarioSchema()
tipousuario_schema = TipousuarioSchema()
