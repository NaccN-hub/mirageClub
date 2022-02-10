from flask import Blueprint

cajas_bp = Blueprint('cajas', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers