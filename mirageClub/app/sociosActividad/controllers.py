from flask import render_template, request, url_for, jsonify, flash, g, abort
import decimal
from werkzeug.utils import redirect

from app.usuarios.decorator import auth_required
from .models import Socioactividad
from ..socios.models import Socio
from ..actividades.models import Actividad
from ..personas.models import Persona
from .schemas import sociosActividad_schema
from app import db


from . import sociosActividad_bp


@sociosActividad_bp.route("/")
@auth_required
def index():
    socioActividad = Socioactividad.get_active()
    persona = Persona.get_active()
    socios = Socio.get_active()
    actividades = Actividad.get_active()

    sociosActivos = []
    for socio in socioActividad:
        sociosActivos.append(Socio.get_by_id(socio.Id_socio))

    listaSocios = []
    for list in socios:
        socio = Socio.get_by_id(list.Id)
        if socio not in sociosActivos:
            listaSocios.append(socio)

    return render_template("sociosActividad/sociosActividad_Home.html", listaSocios=listaSocios, persona=persona, socios=socios, socioActividad=socioActividad, actividades=actividades)


@sociosActividad_bp.route("/nuevo_socioActividad", methods=['POST'])
@auth_required
def nuevo_socioActividad():
    if request.method == 'POST':
        Id_actividad = int(request.form['Id_actividad'])
        Id_socio = int(request.form['Id_socio'])
        Finicio = request.form['Fingreso']

        socioActividad = Socioactividad(
            Id_actividad, Id_socio, Finicio)
        db.session.add(socioActividad)
        db.session.commit()
        socio = Socio.get_by_id(Id_socio)
        flash(
            f"SocioActividad Registrado Correctamente {socio}", "success")
        return redirect(url_for('sociosActividad.index'))


@sociosActividad_bp.route("/nueva_actividad<idSocio>", methods=['POST'])
@auth_required
def nueva_actividad(idSocio):
    if request.method == 'POST':        
        Id_actividad = int(request.form['Id_actividad'])
        Finicio = request.form['Fingreso']
        socioActividad = Socioactividad(
            Id_actividad, idSocio, Finicio)
        db.session.add(socioActividad)
        db.session.commit()

        actividad = Actividad.get_by_id(Id_actividad)
        socio = Socio.get_by_id(idSocio)
        flash(
            f"Actividad Registrada Correctamente {actividad}, Socio {socio}", "success")
        return redirect(url_for('sociosActividad.planillaSocioActividad', idSocio=idSocio))


@sociosActividad_bp.route("/<idSocio>")
@auth_required
def planillaSocioActividad(idSocio):
    nombre = Socio.get_persona(Socio.get_by_id(idSocio).Id_persona)
    # print('id ruta', idSocio)
    id_actividades = []
    actividades = []
    listaActividades = []
    totalActividades = 0 #representa el valor total de las actividades del socio

    try:
        socio = Socioactividad.get_socio(idSocio)
        for s in socio:
            id_actividades.append(s.Id_actividad)
        for id in id_actividades:
            actividades.append(Actividad.get_by_id(id))
        """
        for s in socio:
        actividades.append(Actividad.get_by_id(s.Id_actividad))
        """
    except:
        pass

    dumpActividades = Actividad.get_active()
    for list in dumpActividades:
        if list not in actividades:
            listaActividades.append(list)
    
    for act in actividades: 
        totalActividades = totalActividades + act.Valor
    
    return render_template("sociosActividad/sociosActividad.html", listaActividades=listaActividades, nombre=nombre, actividades=actividades, socio_id=idSocio, totalActividades=totalActividades)


@sociosActividad_bp.route("/borrar_socioActividad_<id>_<actividad>")
@auth_required
def borrar_socioActividad(id, actividad):
    socioActividad = Socioactividad.get_actividad(id, actividad)
    socioActividad.delete()
    actividad = Actividad.get_by_id(actividad)
    socio = Socio.get_by_id(id)
    flash(
        f"Actividad Desactivada Correctamente {actividad}, socio {socio}", "danger")
    return redirect(url_for('sociosActividad.planillaSocioActividad', idSocio=id))
