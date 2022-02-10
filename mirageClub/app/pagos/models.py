from threading import local
from sqlalchemy import func
from sqlalchemy.sql.schema import ForeignKey
from app import db
import locale

# locale.setlocale(locale.LC_TIME, 'es_ES.utf8')


class Pago(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Fecha = db.Column(db.Date, nullable=False)
    Id_deuda = db.Column(db.Integer, ForeignKey('deuda.Id'))
    Monto = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    Descripcion = db.Column(
        db.String(300), default='\ "Descripcion Pago\"', nullable=False)
    Activo = db.Column(db.Boolean, default=True, nullable=False)
    Cerrado = db.Column(db.Boolean, default=True, nullable=False)
    Momento_carga = db.Column(db.Date, nullable=False)

    def __init__(self, Fecha, Id_deuda, Monto, Descripcion):
        self.Fecha = Fecha
        self.Id_deuda = Id_deuda
        self.Monto = Monto
        self.Descripcion = Descripcion

    def get_all():
        return Pago.query.all()

    def get_saldo(id):
        return Pago.query.with_entities(func.sum(Pago.Monto)).filter_by(Id_deuda=id).all()[0][0]

    def get_active():
        return Pago.query.filter_by(Activo=1).all()

    def get_by_id(_id):
        return Pago.query.filter_by(Id=_id).one()
