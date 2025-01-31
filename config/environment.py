import os
import logging

FLASK_SECRET_KEY = os.getenv('SECRET_KEY', "mysecretkey")
DATABASE_PATH = os.getenv('DATABASE_PATH', './data/db/habits.db')
CONFIGURATION_PATH = os.getenv('CONFIGURATION_PATH', '/app/data/config')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()

