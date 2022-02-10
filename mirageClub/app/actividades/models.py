from app import db


class Actividad(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(150), nullable=False)
    Valor = db.Column(db.Numeric(10, 2), nullable=False)
    Descripcion = db.Column(db.String(350))
    Activo = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, Nombre, Valor, Descripcion):
        self.Nombre = Nombre
        self.Valor = Valor
        self.Descripcion = Descripcion

    def __repr__(self):
        return '<Actividad %r>' % self.Nombre

    def get_all():
        return Actividad.query.all()

    def get_active():
        return Actividad.query.filter_by(Activo=1)

    def get_by_id(_id):
        return Actividad.query.filter_by(Id=_id).one()

    def delete(self):
        self.Activo = 0
        db.session.commit()
