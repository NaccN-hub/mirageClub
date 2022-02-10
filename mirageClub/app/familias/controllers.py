from flask import render_template, request, url_for, jsonify, flash
import decimal
from werkzeug.utils import redirect
from app.personas.models import Persona
from app.socios.models import Socio
from app.usuarios.decorator import auth_required

from .models import Familiar
from .schemas import Familia_schema, FamiliaSchema
from app import db

from . import familias_bp

@familias_bp.route("/")
@auth_required
def index():
    familiares = Familiar.get_active()
    socios = Socio.get_all()
    personas = Persona.get_all()
    return render_template("familias.html", familiares=familiares, socios=socios, personas=personas)


@familias_bp.route("/nueva_familia", methods=['POST'])
@auth_required
def nueva_familia():
    if request.method == 'POST':
        Id_persona = int(request.form['Id_persona'])
        Id_socio = int(request.form['Id_socio'])
        Fingreso = request.form['Fingreso']

        familia_nueva = Familiar(Id_persona, Id_socio, Fingreso)
        db.session.add(familia_nueva)
        db.session.commit()

        flash(f"Familia creada correctamente", "success")

        return redirect(url_for('familias.index'))

@familias_bp.route("/borrar_familia_<id>")
@auth_required
def borrar_familia(id):
    familia = Familiar.get_by_id(id)
    familia.delete()
    flash(f"Familia desactivada correctamente", "danger")
    return redirect(url_for('familias.index'))
