from app import db
from ..actividades.models import Actividad
from ..socios.models import Socio
from ..personas.models import Persona
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation, relationship


class Socioactividad(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Id_actividad = db.Column(db.Integer, ForeignKey('actividad.Id'))
    Id_socio = db.Column(db.Integer, ForeignKey('socio.Id'))
    Finicio = db.Column(db.Date, nullable=False)
    Activo = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, Id_actividad, Id_socio, Finicio):
        self.Id_actividad = Id_actividad
        self.Id_socio = Id_socio
        self.Finicio = Finicio

    # def __repr__(self):

    #   def get_all():
    #       return SociosActividad.query.all()
    def get_active():
        return Socioactividad.query.filter_by(Activo=1).group_by(Socioactividad.Id_socio)

    def get_socio(id):
        # print('query',Socioactividad.query.filter_by(Activo=1, Id_socio=id).all())
        return Socioactividad.query.filter_by(Activo=1, Id_socio=id).all()

    def get_actividad(id, actividad):
        return Socioactividad.query.filter_by(Activo=1, Id_socio=id, Id_actividad = actividad).one()

    def get_persona(id):
        return Persona.get_by_id(id).Nombre

    def get_by_id(_id):
        return Socioactividad.query.filter_by(Id=_id).one()

    def delete(self):
        self.Activo = 0
        db.session.commit()
