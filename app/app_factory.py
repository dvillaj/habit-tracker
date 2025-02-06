from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config.logger import LoggerConfig
from config import Config
import os


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    from app.api.security import init_jwt
    from app.database.models import User
    from app.database.setup import create_initial_data

    app = Flask(__name__)
    
    app.config.from_object(config_class)
    init_jwt(app)

     # Configurar logging
    LoggerConfig.configure()
    app.logger = LoggerConfig.get_logger('app')

    app.logger.info(f'Starting app in {Config.FLASK_ENV} environment')

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

    app.logger.info(f'Database URI: {Config.SQLALCHEMY_DATABASE_URI}')

    if not os.path.exists(Config.SQLALCHEMY_DATABASE_URI.split('///')[1]):
        os.makedirs(os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.split('///')[1]), exist_ok=True)

    with app.app_context():
        db.create_all()
        create_initial_data()
    
    login_manager.login_message = "Debes iniciar sesión para acceder a esta página"
    login_manager.login_message_category = "warning"

    return app