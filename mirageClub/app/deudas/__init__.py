from flask import Blueprint

deudas_bp = Blueprint('deudas', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers