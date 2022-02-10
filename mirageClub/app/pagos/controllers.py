from flask import render_template, request, url_for, jsonify, flash, g, abort
import decimal
import pytz
from datetime import datetime
from werkzeug.utils import redirect
from app.deudas.models import Deuda
from app.personas.models import Persona
from app.socios.models import Socio
from app.usuarios.decorator import auth_required
from .models import Pago
from app import db, socios, sociosActividad

from . import pagos_bp


@pagos_bp.route("/")
@auth_required
def index():    
    pagos = Pago.get_all()
    deudas = Deuda.get_all()
    socio = Socio.get_all()
    persona = Persona.get_all()
    return render_template('pagos.html', pagos=pagos, deudas=deudas, socios=socio, personas=persona)
