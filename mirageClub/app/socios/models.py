from app import db
from sqlalchemy import ForeignKey
from ..personas.models import Persona


class Socio(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Id_persona = db.Column(db.Integer, ForeignKey('persona.Id'))
    Fingreso = db.Column(db.Date, nullable=False)
    Activo = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, Id_persona, Fingreso):
        self.Id_persona = Id_persona
        self.Fingreso = Fingreso

    def __repr__(self):
        id = self.Id_persona
        persona = Socio.get_persona(id)
        return persona

    def get_all():
        return Socio.query.all()

    def get_persona(id):
        return Persona.get_by_id(id).Nombre

    def get_active():
        return Socio.query.filter_by(Activo=1)

    def get_by_id(_id):
        return Socio.query.filter_by(Id=_id).one()

    def delete(self):
        self.Activo = 0
        db.session.commit()
