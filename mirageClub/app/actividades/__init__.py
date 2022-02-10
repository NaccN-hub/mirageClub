from flask import Blueprint

actividades_bp = Blueprint('actividades', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers
