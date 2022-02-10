from flask import Blueprint

personas_bp = Blueprint('personas', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers