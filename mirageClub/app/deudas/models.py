from app import db
from sqlalchemy import ForeignKey
from ..socios.models import Socio
from ..personas.models import Persona
import locale

# locale.setlocale(locale.LC_TIME, 'es_ES.utf8')


class Deuda(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Id_socio = db.Column(db.Integer, ForeignKey('socio.Id'))
    Descripcion = db.Column(
        db.String(300), default='\ "Cuota Social\"', nullable=False)
    Mes = db.Column(db.Date, nullable=False)
    Importe = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    Abonada = db.Column(db.Boolean, default=False, nullable=False)
    Fgeneracion = db.Column(db.Date, nullable=False)

    def __init__(self, Id_socio, Descripcion, Mes, Importe):
        self.Id_socio = Id_socio
        self.Descripcion = Descripcion
        self.Mes = Mes
        self.Importe = Importe

    def __repr__(self):
        socio = self.Id_socio
        id = Socio.get_by_id(socio).Id_persona
        persona = Socio.get_persona(id)
        return persona

    def get_all():
        return Deuda.query.all()

    def get_active():
        return Deuda.query.filter_by(Abonada=0).all()

    def get_billed():
        return Deuda.query.filter_by(Abonada=1).all()

    def get_by_id(_id):
        return Deuda.query.filter_by(Id=_id).one()

    def abonar(self):
        self.Abonada = 1
        db.session.commit()

    def get_persona(id):
        return Persona.get_by_id(id).Nombre
