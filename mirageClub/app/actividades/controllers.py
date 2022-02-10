from flask import render_template, request, url_for, jsonify, flash, abort, g
import decimal
from werkzeug.utils import redirect

from app.usuarios.decorator import auth_required
from .models import Actividad
from .schemas import actividad_schema, ActividadSchema
from app import db

from . import actividades_bp


@actividades_bp.route("/")
@auth_required
def index():
    actividad = Actividad.get_active()
    return render_template("actividades/actividades.html", actividad=actividad)


@actividades_bp.route("/nueva_actividad", methods=['POST'])
@auth_required
def nueva_actividad():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Valor = request.form['Valor']
        Descripcion = request.form['Descripcion']

        actividad = Actividad(Nombre, Valor, Descripcion)
        db.session.add(actividad)
        db.session.commit()
        flash(f"Actividad Guardada Correctamente {actividad}", "success")
        return redirect(url_for('actividades.index'))


@actividades_bp.route("/borrar_actividad_<id>")
@auth_required
def borrar_actividad(id):
    actividad = Actividad.get_by_id(id)
    actividad.delete()
    flash(f"Actividad Desactivada Correctamente {actividad}", "danger")
    return redirect(url_for('actividades.index'))


@actividades_bp.route("/modal_editar", methods=['POST'])
@auth_required
def modal_editar():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        actividad = actividad_schema.dump(
            Actividad.get_by_id(data['idActividad']))
        return jsonify(actividad), 200


@actividades_bp.route("/editar_actividad", methods=['POST'])
@auth_required
def editar_actividad():
    id = request.form['idActividad']
    actividad = Actividad.get_by_id(id)
    actividad.Nombre = request.form['Nombre']
    actividad.Valor = request.form['Valor']
    actividad.Descripcion = request.form['Descripcion']
    db.session.commit()
    flash(f"Actividad Editada Correctamente {actividad}", "info")
    # URL ?? - NO AJAX
    return redirect(url_for('actividades.index'))


@actividades_bp.route("/modal_ver", methods=['POST'])
@auth_required
def modal_ver():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        actividad = actividad_schema.dump(
            Actividad.get_by_id(data['idActividad']))
        return jsonify(actividad), 200
