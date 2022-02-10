from flask import render_template, request, url_for, jsonify, flash, g, abort
import decimal
import pytz
from datetime import datetime
from werkzeug.utils import redirect

from app.usuarios.decorator import auth_required
from .models import Deuda
from ..personas.models import Persona
from ..socios.models import Socio
from ..sociosActividad.models import Socioactividad
from ..actividades.models import Actividad
from ..pagos.models import Pago
from .schemas import deuda_schema
from app import db

from . import deudas_bp

tz_arg = pytz.timezone('America/Argentina/Buenos_Aires')


@deudas_bp.route("/")
@auth_required
def index():
    deuda_todos = Deuda.get_all()
    socio = Socio.get_all()
    persona = Persona.get_all()

    return render_template("deudas/deudas.html", deudas=deuda_todos, socios=socio, personas=persona)


@deudas_bp.route("/abonados")
@auth_required
def abonados():
    deuda_abonados = Deuda.get_billed()
    socio = Socio.get_all()
    persona = Persona.get_all()

    return render_template("deudas/deudas.html", deudas=deuda_abonados, socios=socio, personas=persona)


@deudas_bp.route("/activos")
@auth_required
def activos():
    deuda_activos = Deuda.get_active()
    socio = Socio.get_all()
    persona = Persona.get_all()

    return render_template("deudas/deudas.html", deudas=deuda_activos, socios=socio, personas=persona)


@deudas_bp.route("/batch_deuda", methods=['POST'])
@auth_required
def batch_deuda():
    if request.method == 'POST':
        deuda = Deuda.get_all()
        socioActividad = Socioactividad.get_active()
        actividades = Actividad.get_active()
        Mes = datetime.strptime(
            request.form['Mes'], "%m/%Y")  # FORM AÑO-MES SOLO
        Descripcion = 'Cuota Social'  # form?

    sociosActivos = []
    for deuda_socio in deuda:
        # print('id', deuda_socio.Id_socio, 'mes', deuda_socio.Mes)
        socio = Socioactividad.get_socio(deuda_socio.Id_socio)
        fecha = deuda_socio.Mes.strftime("%Y-%m-%d")
        sociosActivos.append([socio, fecha])
    # print('socios', sociosActivos)
    listaSocios = []  # Excluye los datos existentes para evitar repeticion
    for list in socioActividad:
        # print('list', list.Id_socio)
        lista_socio = Socioactividad.get_socio(list.Id_socio)
        lista_fecha = Mes.strftime("%Y-%m-%d")
        socio_Mes = [lista_socio, lista_fecha]
        # print(socio_Mes)
        if socio_Mes not in sociosActivos:
            listaSocios.append(lista_socio)
    # print('lista', listaSocios)

    # print(range(len(listaSocios)))
    for i in range(len(listaSocios)):
        # [ lista de socioactividad ] [0] primer objeto del socio .id_socio
        Id_socio = listaSocios[i][0].Id_socio
        # print('importe', Id_socio)
        Importe = 0
        for soc in listaSocios[i]:
            # print(soc)
            for act in actividades:
                if soc.Id_actividad == act.Id:
                    Importe += act.Valor

        deuda = Deuda(Id_socio, Descripcion, Mes, Importe)
        db.session.add(deuda)

    db.session.commit()
    flash(
        f"Deudas Generadas Correctamente - {Mes.strftime('%B %Y').capitalize()}", "success")
    return redirect(url_for('deudas.index'))


@ deudas_bp.route("/abonar_deuda", methods=['POST'])
@auth_required
def abonar_deuda():
    deuda_id = request.form['idDeuda']
    deuda = Deuda.get_by_id(deuda_id)
    fecha = datetime.now(tz_arg).strftime("%Y-%m-%d")
    monto = request.form['Monto']
    saldo = Pago.get_saldo(deuda_id)
    # print('\nfecha', fecha, '\nid', deuda_id,
    #       '\nmonto', monto, '\ncuota', deuda.Importe, '\nsaldo', saldo)
    pago = Pago(fecha, deuda_id, monto, deuda.Descripcion)

    try:
        total = float(monto) + float(saldo)
    except:
        total = float(monto)
    if total == deuda.Importe:
        deuda.abonar()
        flash(
            f"Deuda Abonada Correctamente {deuda} - {deuda.Mes.strftime('%B-%Y').capitalize()}", "success")
    else:
        flash(
            f"Pago Cargado Correctamente:  Cuota->{deuda.Mes.strftime('%B-%Y').capitalize()}, Socio->{deuda}, Monto->{monto}", "success")

    db.session.add(pago)
    db.session.commit()
    return redirect(url_for('deudas.index'))


@deudas_bp.route("/borrar_deuda_<id>")
@auth_required
def borrar_deuda(id):
    deuda = Deuda.get_by_id(id)
    db.session.delete(deuda)
    db.session.commit()

    flash(f"Deuda Eliminada Correctamente {deuda} - {deuda.Mes}", "danger")
    return redirect(url_for('deudas.index'))


@ deudas_bp.route("/modal_editar", methods=['POST'])
@auth_required
def modal_editar():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        deuda = deuda_schema.dump(
            Deuda.get_by_id(data['idDeuda']))
        return jsonify(deuda), 200


@ deudas_bp.route("/modal_ver", methods=['POST'])
@auth_required
def modal_ver():
    if request.method == 'POST':
        data = request.get_json()
        data = data[0]
        deuda = deuda_schema.dump(
            Deuda.get_by_id(data['idDeuda']))
        sum = Pago.get_saldo(data['idDeuda'])
        try:
            pago = Pago.get_by_id(data['idPago'])
            deuda['Fechapago'] = pago.Fecha.strftime('%Y-%m-%d')
            deuda['Monto'] = float(pago.Monto)
        except:
            pass
        # print('id', data['idDeuda'], '\ndeuda',
        #       deuda['Importe'], '\nsum', str(sum))
        try:
            valor = round(deuda['Importe'] - float(sum), 2)
            deuda['Maxinput'] = valor
        except:
            deuda['Maxinput'] = deuda['Importe']
        return jsonify(deuda), 200


@ deudas_bp.route("/editar_deuda", methods=['POST'])
@auth_required
def editar_deuda():
    id = request.form['idDeuda']
    # print(id)
    deuda = Deuda.get_by_id(id)
    deuda.Descripcion = request.form['Descripcion']
    deuda.Mes = request.form['Mes']
    deuda.Importe = request.form['Importe']

    db.session.commit()
    flash(f"Deuda Editada Correctamente {deuda}", "info")
    return redirect(url_for('deudas.index'))
