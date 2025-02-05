from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import timedelta
import logging.config
import logging
import yaml
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    from app.api.security import init_jwt
    from app.database.models import User

    app = Flask(__name__)
    
    app.config.from_object(config_class)
    init_jwt(app)

    # Configurar logging

    with open('logging_config.yaml') as f:
        config = yaml.safe_load(f.read().replace('${LOG_LEVEL}', os.getenv('LOG_LEVEL', 'INFO')))
        logging.config.dictConfig(config)
    
    app.logger = logging.getLogger('app')

    app.logger.debug(f'Starting app in {app.config["FLASK_ENV"]} environment')

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Registrar blueprints
    from app.auth.routes import auth_bp
    from app.habits.routes import habits_bp
    from app.api.routes import api_bp
    from app.setup.routes import setup_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(habits_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(setup_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Crear tablas en la base de datos
    #import os
    #from config import Config

    app.logger.error(f'Database URI: {Config.SQLALCHEMY_DATABASE_URI}')

    if not os.path.exists(Config.SQLALCHEMY_DATABASE_URI.split('///')[1]):
        os.makedirs(os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.split('///')[1]), exist_ok=True)

    with app.app_context():
        db.create_all()
        create_initial_data()
    
    login_manager.login_message = "Debes iniciar sesión para acceder a esta página"
    login_manager.login_message_category = "warning"

    # Configurar sesión permanente
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)

    return app


def create_initial_data():
    from app.database.models import ExampleHabit
    if ExampleHabit.query.count() == 0:
        examples = [
            ExampleHabit(title="Ejercicio", description="30 minutos de actividad física", icon="exercise.svg"),
            ExampleHabit(title="Leer", description="20 páginas diarias", icon="book.svg"),
            ExampleHabit(title="Meditar", description="10 minutos de meditación", icon="meditation.svg")
        ]
        db.session.bulk_save_objects(examples)
        db.session.commit()