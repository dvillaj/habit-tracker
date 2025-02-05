import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    # Configuración base
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getenv('DATABASE_PATH', BASE_DIR / 'instance'), 'habits.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_WORKERS = int(os.getenv('FLASK_WORKERS', 4))
    
    # Configuración de uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'svg'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024    