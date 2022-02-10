from app import db


class Persona(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(150), nullable=False)
    Dni = db.Column(db.String(11), nullable=False)
    Direccion = db.Column(db.String(200))
    Fnacimiento = db.Column(db.Date, nullable=False)
    Sexo = db.Column(db.Boolean, default=True, nullable=False)
    Telefono = db.Column(db.String(50))
    Email = db.Column(db.String(100))
    Activo = db.Column(db.Boolean, default=True, nullable=False)
    Fcarga = db.Column(db.Date, nullable=False)

    def __init__(self, Nombre, Dni, Direccion, Fnacimiento, Sexo, Telefono, Email):
        self.Nombre = Nombre
        self.Dni = Dni
        self.Direccion = Direccion
        self.Fnacimiento = Fnacimiento
        self.Sexo = Sexo
        self.Telefono = Telefono
        self.Email = Email

    def __repr__(self):
        return '<%r>' % self.Nombre

    def get_all():
        return Persona.query.all()

    def get_active():
        return Persona.query.filter_by(Activo=1)

    def get_by_id(_id):
        return Persona.query.filter_by(Id=_id).one()

    def delete(self):
        self.Activo = 0
        db.session.commit()
