from flask import Blueprint

familias_bp = Blueprint('familias', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers
