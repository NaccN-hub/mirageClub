from app import db
from sqlalchemy import ForeignKey

from app.sociosActividad.models import Socioactividad

from ..actividades.models import Actividad
from ..deudas.models import Deuda


class Usuario(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Contrasenia = db.Column(db.String(200), nullable=False)
    Id_socio = db.Column(db.Integer, ForeignKey('socio.Id'))
    Id_tipousuario = db.Column(db.Integer, ForeignKey('tipousuario.Id'))
    Fcarga = db.Column(db.Date, nullable=False)

    def __init__(self, Nombre, Contrasenia, Id_socio, Id_tipousuario, Fcarga):
        self.Nombre = Nombre
        self.Contrasenia = Contrasenia
        self.Id_socio = Id_socio
        self.Id_tipousuario = Id_tipousuario
        self.Fcarga = Fcarga

    def __repr__(self):
        return self.Nombre

    def get_deudas(self):
        return Deuda.query.filter_by(Id_socio=self.Id_socio)

    def get_active(self):
        return Deuda.query.filter_by(Id_socio=self.Id_socio, Abonada=0)

    def get_billed(self):
        return Deuda.query.filter_by(Id_socio=self.Id_socio, Abonada=1)

    def get_actividades(self):
        return Socioactividad.query.filter_by(Activo=1, Id_socio=self.Id_socio).all()

    def get_by_name(username):
        return Usuario.query.filter_by(Nombre=username).one()

    # EL SALT GENERADO EN LOGIN SIEMPRE ES DISTINTO, NO MATCHEA
    # def auth(usr, pwd):
    #     return Usuario.query.filter_by(Nombre=usr, Contrasenia=pwd).one()

    def get_by_id(id):
        return Usuario.query.filter_by(Id=id).one()


class Tipousuario(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Descripcion = db.Column(db.String(200), nullable=False)

    def __init__(self, Nombre, Descripcion):
        self.Nombre = Nombre
        self.Descripcion = Descripcion

    def __repr__(self):
        return '<%r>' % self.Nombre
