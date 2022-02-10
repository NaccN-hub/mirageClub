from flask import Blueprint

sociosActividad_bp = Blueprint(
    'sociosActividad', __name__, template_folder='templates')

# NO BORRAR vvvv
from . import controllers #registrar rutas del controlador de socioActividad.