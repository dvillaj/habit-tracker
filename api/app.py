from flask import Flask
from api.routes import register_routes


def create_app(config=None):
    app = Flask(__name__, template_folder='../templates')
    
    # Basic configuration
    if config:
        app.config.update(config)
    
    # Registrar las rutas
    register_routes(app)
  
    return app