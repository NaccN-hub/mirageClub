from flask import render_template, request, url_for, jsonify, flash, session, g, abort
import decimal
import bcrypt
from werkzeug.utils import redirect
from app.actividades.models import Actividad

from app.deudas.models import Deuda
from app.familias.models import Familiar
from app.personas.models import Persona
from app.socios.models import Socio
from app.usuarios.decorator import auth_required
from .models import Usuario, Tipousuario
from .schemas import usuario_schema, tipousuario_schema
from app import db

from . import usuarios_bp


@usuarios_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        try:
            user = Usuario.get_by_name(username)
            if user.Contrasenia == password:
                session['user_id'] = user.Id
                flash(
                    f"Bienvenido {user}", "success")
                flash('Por favor cambie su contrasenia', "warning")
                return redirect(url_for('usuarios.change_password'))
            else:
                if bcrypt.checkpw(password.encode('utf-8'), user.Contrasenia.encode('utf-8')):
                    session['user_id'] = user.Id
                    flash(
                        f"Bienvenido {user}", "success")
                    return redirect(url_for('index'))
                3/0  # ERROR PARA SALIR POR EXCEPT
        except:
            flash(
                f"Usuario o contraseña incorrectos, vuelva a intentar", "danger")
            return redirect(url_for('usuarios.login'))

    return render_template("usuarios/login.html")


@usuarios_bp.route("/logout")
def logout():
    session.pop('user_id', None)
    flash(
        "Cierre de Sesión", "success")

    return redirect(url_for('index'))


@usuarios_bp.route("/password", methods=['GET', 'POST'])
def change_password():
    if not g.user:
        abort(401)
    if request.method == 'POST':
        password = request.form['nuevapass'].encode('utf-8')
        user = Usuario.get_by_id(g.user.Id)
        hashPwd = bcrypt.hashpw(password, bcrypt.gensalt(12))
        user.Contrasenia = hashPwd
        db.session.commit()
        return redirect(url_for('index'))

    return render_template(('usuarios/cambiar_contrasenia.html'))


@usuarios_bp.route("/")
def index():
    if not g.user:
        abort(401)
    deuda_todos = Usuario.get_deudas(g.user)
    socio = Socio.get_all()
    persona = Persona.get_all()

    return render_template("usuarios/deudasSocio.html", deudas=deuda_todos, socios=socio, personas=persona)


@usuarios_bp.route("/abonados")
def abonados():
    if not g.user:
        abort(401)
    deuda_abonados = Usuario.get_billed(g.user)
    socio = Socio.get_all()
    persona = Persona.get_all()

    return render_template("usuarios/deudasSocio.html", deudas=deuda_abonados, socios=socio, personas=persona)


@usuarios_bp.route("/activos")
def activos():
    if not g.user:
        abort(401)
    deuda_activos = Usuario.get_active(g.user)
    socio = Socio.get_all()
    persona = Persona.get_all()

    return render_template("usuarios/deudasSocio.html", deudas=deuda_activos, socios=socio, personas=persona)


@usuarios_bp.route("/perfil")
def profile():
    if not g.user:
        abort(401)
    socio = Socio.get_by_id(g.user.Id_socio)
    cliente = Persona.get_by_id(socio.Id_persona)
    actividades = Usuario.get_actividades(g.user)
    listact = Actividad.get_all()
    familiares = Familiar.get_socio(g.user.Id_socio)
    personas = Persona.get_all()

    return render_template("usuarios/perfil.html", cliente=cliente, actividades=actividades, listact=listact, familiares=familiares, personas=personas)
