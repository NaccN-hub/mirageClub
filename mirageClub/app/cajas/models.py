from sqlalchemy import func
from sqlalchemy.sql.schema import ForeignKey
from app import db
import locale


class Ingreso(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Id_socio = db.Column(db.Integer, ForeignKey('socio.Id'), nullable=True)
    Fecha = db.Column(db.Date, nullable=False)
    Monto = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    Descripcion = db.Column(db.String(300), nullable=False)
    Eliminado = db.Column(db.Boolean, default=True, nullable=False)
    Fcarga = db.Column(db.Date, nullable=False)

    def __init__(self, Id_socio, Fecha, Monto, Descripcion):
        self.Id_socio = Id_socio
        self.Fecha = Fecha
        self.Monto = Monto
        self.Descripcion = Descripcion

    def get_all():
        return Ingreso.query.all()

    def get_active():
        return Ingreso.query.filter_by(Eliminado=1).all()

    def get_by_id(_id):
        return Ingreso.query.filter_by(Id=_id).one()
    
    def cerrar(self):
        self.Eliminado = 0
        db.session.commit()


class Egreso(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Id_rubro = db.Column(db.Integer, ForeignKey('rubro.Id'))
    Fecha = db.Column(db.Date, nullable=False)
    Importe = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    Descripcion = db.Column(db.String(200), nullable=False)
    Fcarga = db.Column(db.Date, nullable=False)

    def __init__(self, Id_rubro, Fecha, Importe, Descripcion):
        self.Id_rubro = Id_rubro
        self.Fecha = Fecha
        self.Importe = Importe
        self.Descripcion = Descripcion

    def get_all():
        return Egreso.query.all()

    def get_active():
        return Egreso.query.filter_by(Eliminado=1).all()

    def get_by_id(_id):
        return Egreso.query.filter_by(Id=_id).one()


class Rubro(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(200), nullable=False)
    Eliminado = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, Nombre):
        self.Nombre = Nombre

    def get_all():
        return Rubro.query.all()

    def get_active():
        return Rubro.query.filter_by(Eliminado=1).all()

    def get_by_id(_id):
        return Rubro.query.filter_by(Id=_id).one()
    
    def eliminar(self):
        self.Eliminado = 0
        db.session.commit()
