from flask import Blueprint

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers