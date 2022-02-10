from app import db
from ..personas.models import Persona
from ..socios.models import Socio
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation, relationship

class Familiar(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Id_persona = db.Column(db.Integer, ForeignKey('persona.Id'))
    Id_socio = db.Column(db.Integer, ForeignKey('socio.Id'))
    Fingreso = db.Column(db.Date)
    Activo = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, Id_persona, Id_socio, Fingreso):
        self.Id_persona = Id_persona
        self.Id_socio = Id_socio
        self.Fingreso = Fingreso

    def get_all():
        return Familiar.query.all()

    def get_active():
        return Familiar.query.filter_by(Activo=1)

    def get_by_id(_id):
        return Familiar.query.filter_by(Id=_id).one()

    def get_persona(id):
        return Persona.get_by_id(id).Nombre
    
    def get_socio(id):
        return Familiar.query.filter_by(Activo=1, Id_socio=id).all()
    
    def delete(self):
        self.Activo = 0
        db.session.commit()


    