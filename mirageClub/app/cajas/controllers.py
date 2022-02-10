from flask import render_template, request, url_for, jsonify, flash, g, abort
import decimal
import pytz
from datetime import datetime
from werkzeug.utils import redirect
from app.deudas.models import Deuda
from app.personas.models import Persona
from app.socios.models import Socio
from app.pagos.models import Pago
from app.usuarios.decorator import auth_required
from .models import Ingreso, Egreso, Rubro
from .schemas import ingreso_schema, egreso_schema, rubro_schema
from app import db

from . import cajas_bp


@cajas_bp.route("/")
@auth_required
def index():
    pagos = Pago.get_all()
    deudas = Deuda.get_all()
    socio = Socio.get_all()
    persona = Persona.get_all()
    ingresos = Ingreso.get_all()
    egresos = Egreso.get_all()
    rubros = Rubro.get_all()
    return render_template('cajas.html', pagos=pagos, deudas=deudas, socios=socio, personas=persona, ingresos=ingresos, egresos=egresos, rubros=rubros)


@cajas_bp.route("/ingresos")  # INGRESOS
@auth_required
def ingresos():
    lista = Ingreso.get_all()
    socio = Socio.get_all()
    listasocio = Socio.get_active()
    persona = Persona.get_all()
    return render_template('ingresos.html', ingresos=lista, socios=socio, listasocio=listasocio, personas=persona)


@cajas_bp.route("/ingresos/add", methods=['POST'])
@auth_required
def ingresos_add():
    if request.method == 'POST':
        try:
            Id_socio = int(request.form['Id_socio'])
        except:
            Id_socio = None
        Fecha = request.form['Fecha']
        Monto = request.form['Monto']
        Descripcion = request.form['Descripcion']

        ingreso = Ingreso(Id_socio, Fecha, Monto, Descripcion)
        db.session.add(ingreso)
        db.session.commit()
        flash(f"Ingreso Registrado Correctamente {ingreso}", "success")
        return redirect(url_for('cajas.ingresos'))


@cajas_bp.route("/ingresos/modal_ver", methods=['POST'])
@auth_required
def ingresos_modal_ver():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]

        ingreso = ingreso_schema.dump(
            Ingreso.get_by_id(data['idIngreso']))
        return jsonify(ingreso), 200


@cajas_bp.route("/ingresos/edit", methods=['POST'])
@auth_required
def ingresos_edit():
    id = request.form['idIngreso']
    ingreso = Ingreso.get_by_id(id)
    ingreso.Descripcion = request.form['Descripcion']

    db.session.commit()
    flash(f"Ingreso Editado Correctamente {ingreso}", "info")
    return redirect(url_for('cajas.ingresos'))


@cajas_bp.route("/egresos")  # EGRESOS
@auth_required
def egresos():
    lista = Egreso.get_all()
    rubros = Rubro.get_all()
    listarubro = Rubro.get_active()
    return render_template('egresos.html', egresos=lista, rubros=rubros, listarubro=listarubro)


@cajas_bp.route("/egresos/add", methods=['POST'])
@auth_required
def egresos_add():
    if request.method == 'POST':
        Id_rubro = int(request.form['Id_rubro'])
        Fecha = request.form['Fecha']
        Importe = request.form['Importe']
        Descripcion = request.form['Descripcion']

        egreso = Egreso(Id_rubro, Fecha, Importe, Descripcion)
        db.session.add(egreso)
        db.session.commit()
        flash(f"Egreso Registrado Correctamente {egreso}", "success")
        return redirect(url_for('cajas.egresos'))


@cajas_bp.route("/egresos/modal_ver", methods=['POST'])
@auth_required
def egresos_modal_ver():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        egreso = egreso_schema.dump(
            Egreso.get_by_id(data['idEgreso']))
        return jsonify(egreso), 200


@cajas_bp.route("/egresos/edit", methods=['POST'])
@auth_required
def egresos_edit():
    id = request.form['idEgreso']
    egreso = Egreso.get_by_id(id)
    egreso.Descripcion = request.form['Descripcion']

    db.session.commit()
    flash(f"Egreso Editado Correctamente {egreso}", "info")
    return redirect(url_for('cajas.egresos'))


@cajas_bp.route("/egresos/rubros")  # RUBROS
@auth_required
def rubros():
    lista = Rubro.get_all()
    return render_template('rubros.html', rubros=lista)


@cajas_bp.route("/egresos/rubros/add", methods=['POST'])
@auth_required
def rubros_add():
    if request.method == 'POST':
        Nombre = request.form['Nombre']

        rubro = Rubro(Nombre)
        db.session.add(rubro)
        db.session.commit()
        flash(f"Rubro Registrado Correctamente {rubro}", "success")
        return redirect(url_for('cajas.rubros'))


@cajas_bp.route("/egresos/rubros/modal_ver", methods=['POST'])
@auth_required
def rubros_modal_ver():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        rubro = rubro_schema.dump(
            Rubro.get_by_id(data['idRubro']))
        return jsonify(rubro), 200


@cajas_bp.route("/egresos/rubros/edit", methods=['POST'])
@auth_required
def rubros_edit():
    id = request.form['idRubro']
    rubro = Rubro.get_by_id(id)
    rubro.Nombre = request.form['Nombre']

    db.session.commit()
    flash(f"Rubro Editado Correctamente {rubro}", "info")
    return redirect(url_for('cajas.rubros'))
