from flask import Flask, render_template, session, g
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields


db = SQLAlchemy()
ma = Marshmallow()


def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    # Load the config file specified by the APP environment variable
    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/miragedb"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BD2021:BD2021itec@143.198.156.171/MirageDB'

    app.config['SECRET_KEY'] = 'hsjkahdasfghfdshgfdshgfdshgdfsg'

    db.init_app(app)

    register_before_request(app)

    app.add_url_rule('/', 'index', index)
    # CARGAR LOS BLUEPRINTS CON NOMBRE DE RUTA
    from .actividades import actividades_bp
    app.register_blueprint(actividades_bp, url_prefix='/actividades')
    from .personas import personas_bp
    app.register_blueprint(personas_bp, url_prefix='/personas')
    from .socios import socios_bp
    app.register_blueprint(socios_bp, url_prefix='/socios')
    from .deudas import deudas_bp
    app.register_blueprint(deudas_bp, url_prefix='/deudas')
    from .sociosActividad import sociosActividad_bp
    app.register_blueprint(sociosActividad_bp, url_prefix='/socioActividad')
    from .pagos import pagos_bp
    app.register_blueprint(pagos_bp, url_prefix='/pagos')
    from .cajas import cajas_bp
    app.register_blueprint(cajas_bp, url_prefix='/cajas')
    from .familias import familias_bp
    app.register_blueprint(familias_bp, url_prefix='/familias')

    from .usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

    register_error_handlers(app)

    return app


def index():
    return render_template("base_template.html")


def register_before_request(app):
    @app.before_request
    def before_request():
        from app.usuarios.models import Usuario
        g.user = ''
        if 'user_id' in session:
            user = Usuario.get_by_id(session['user_id'])
            g.user = user


def register_error_handlers(app):
    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def error_403_handler(e):
        return render_template('403.html'), 403

    @app.errorhandler(401)
    def error_401_handler(e):
        return render_template('401.html'), 401
