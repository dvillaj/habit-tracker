import os

class AppConfig:
    DATABASE_PATH = 'DATABASE_PATH'
    CONFIGURATION_PATH = 'CONFIGURATION_PATH'
    LOG_LEVEL = 'LOG_LEVEL'

    FLASH_SECRET_KEY = 'SECRET_KEY'
    FLASK_ENV = 'FLASK_ENV'
    FLASK_DEBUG = 'FLASK_DEBUG'
    FLASK_HOST = 'FLASK_HOST'
    FLASK_PORT = 'FLASK_PORT'

    @staticmethod
    def validate(config):
        if not config[AppConfig.DATABASE_PATH]:
            raise ValueError("DATABASE_PATH environment variable is required")

        if not config[AppConfig.CONFIGURATION_PATH]:
            raise ValueError("CONFIGURATION_PATH environment variable is required")
        

    @staticmethod
    def config():
        config = {
            AppConfig.DATABASE_PATH: os.getenv('DATABASE_PATH'),
            AppConfig.FLASH_SECRET_KEY: os.getenv('FLASK_SECRET_KEY', 'prod-secret-key'),
            AppConfig.FLASK_ENV: os.getenv('FLASK_ENV', 'production'),
            AppConfig.FLASK_DEBUG: os.getenv('FLASK_DEBUG', '0'),
            AppConfig.LOG_LEVEL: os.getenv('LOG_LEVEL', 'INFO'),
            AppConfig.CONFIGURATION_PATH: os.getenv('CONFIGURATION_PATH'),
            AppConfig.FLASK_HOST: os.getenv('FLASK_HOST', '127.0.0.1'),
            AppConfig.FLASK_PORT: int(os.getenv('FLASK_PORT', 5000))
        }

        AppConfig.validate(config)

        return config
