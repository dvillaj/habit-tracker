import os
import logging

DATABASE_PATH = os.getenv('DATABASE_PATH', 'habits.db')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()

class LoggerConfig:
    @staticmethod
    def configure_logging():

        logging.basicConfig(
            format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S %z',
            level=getattr(logging, LOG_LEVEL, logging.DEBUG)
        )
