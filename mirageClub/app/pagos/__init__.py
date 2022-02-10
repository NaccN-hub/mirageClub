from flask import Blueprint

pagos_bp = Blueprint('pagos', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers