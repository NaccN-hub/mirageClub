from flask import render_template, request, url_for, jsonify, flash, g, abort
import decimal
from werkzeug.utils import redirect
from app.sociosActividad.models import Socioactividad

from app.usuarios.decorator import auth_required
from .models import Socio
from ..personas.models import Persona
from .schemas import socio_schema
from app import db

from . import socios_bp


@socios_bp.route("/")
@auth_required
def index():
    socio = Socio.get_active()
    persona = Persona.get_active()

    sociosActivos = []
    for soc in socio:
        sociosActivos.append(Persona.get_by_id(soc.Id_persona))

    listaPersonas = []
    for list in persona:
        if list not in sociosActivos:
            listaPersonas.append(list)

    return render_template("socios/socios.html", socio=socio, listaPersonas=listaPersonas, persona=persona)


@socios_bp.route("/nuevo_socio", methods=['POST'])
@auth_required
def nuevo_socio():
    if request.method == 'POST':
        Id_persona = int(request.form['Id_persona'])
        Fingreso = request.form['Fingreso']

        socio = Socio(Id_persona, Fingreso)
        db.session.add(socio)
        db.session.commit()
        flash(f"Socio Registrado Correctamente <' {socio} '>", "success")
        return redirect(url_for('socios.index'))


@socios_bp.route("/borrar_socio_<id>")
@auth_required
def borrar_socio(id):
    check = Socioactividad.get_socio(id)
    socio = Socio.get_by_id(id)
    # print(check)
    if len(check) > 0:
        flash(f"No se puede borrar un socio si tiene actividades registradas", "info")
        return redirect(url_for('socios.index'))
    else:
        socio.delete()
        flash(f"Socio Desactivado Correctamente {socio}", "danger")
        return redirect(url_for('socios.index'))


@socios_bp.route("/modal_editar", methods=['POST'])
@auth_required
def modal_editar():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        socio = socio_schema.dump(
            Socio.get_by_id(data['idSocio']))
        return jsonify(socio), 200


@socios_bp.route("/modal_ver", methods=['POST'])
@auth_required
def modal_ver():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        socio = socio_schema.dump(
            Socio.get_by_id(data['idSocio']))
        return jsonify(socio), 200


@socios_bp.route("/editar_socio", methods=['POST'])
@auth_required
def editar_socio():
    id = request.form['idSocio']
    socio = Socio.get_by_id(id)
    socio.Id_persona = int(request.form['Id_persona'])
    socio.Fingreso = request.form['Fingreso']

    db.session.commit()
    flash(f"Socio Editado Correctamente {socio}", "info")
    return redirect(url_for('socios.index'))
