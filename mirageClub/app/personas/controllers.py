from flask import render_template, request, url_for, jsonify, flash, g, abort
import decimal
from werkzeug.utils import redirect

from app.usuarios.decorator import auth_required
from .models import Persona
from .schemas import persona_schema, persona_simple_schema
from app import db

from . import personas_bp


@personas_bp.route("/")
@auth_required
def index():
    persona = Persona.get_active()
    return render_template("personas/personas.html", persona=persona)


@personas_bp.route("/nueva_persona", methods=['POST'])
@auth_required
def nueva_persona():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Dni = request.form['Dni']
        Direccion = request.form['Direccion']
        Fnacimiento = request.form['Fnacimiento']
        Sexo = int(request.form['Sexo'])
        Telefono = request.form['Telefono']
        Email = request.form['Email']

        persona = Persona(Nombre, Dni, Direccion, Fnacimiento,
                          Sexo, Telefono, Email)
        db.session.add(persona)
        db.session.commit()
        flash(f"Persona Registrada Correctamente {persona}", "success")
        return redirect(url_for('personas.index'))


@personas_bp.route("/borrar_persona_<id>")
@auth_required
def borrar_persona(id):
    persona = Persona.get_by_id(id)
    persona.delete()
    flash(f"Persona Desactivada Correctamente {persona}", "danger")
    return redirect(url_for('personas.index'))


@personas_bp.route("/modal_editar", methods=['POST'])
@auth_required
def modal_editar():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        persona = persona_schema.dump(
            Persona.get_by_id(data['idPersona']))
        return jsonify(persona), 200


@personas_bp.route("/modal_ver", methods=['POST'])
@auth_required
def modal_ver():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        persona = persona_schema.dump(
            Persona.get_by_id(data['idPersona']))
        return jsonify(persona), 200


@personas_bp.route("/editar_persona", methods=['POST'])
@auth_required
def editar_persona():
    id = request.form['idPersona']
    persona = Persona.get_by_id(id)
    persona.Nombre = request.form['Nombre']
    persona.Dni = request.form['Dni']
    persona.Direccion = request.form['Direccion']
    persona.Fnacimiento = request.form['Fnacimiento']
    persona.Sexo = int(request.form['Sexo'])
    persona.Telefono = request.form['Telefono']
    persona.Email = request.form['Email']

    db.session.commit()
    flash(f"Persona Editada Correctamente {persona}", "info")
    return redirect(url_for('personas.index'))
