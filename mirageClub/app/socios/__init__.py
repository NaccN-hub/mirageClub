from flask import Blueprint

socios_bp = Blueprint('socios', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers