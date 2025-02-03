from pathlib import Path
from config.app_config import AppConfig
import logging
import logging.config
import yaml
import traceback
import os

class LoggerConfig:
    
    CONFIG_FILE_NAME = "logging_config.yaml"
    LOG_LEVEL_PLACEHOLDER = "${LOG_LEVEL}"

    def __init__(self):
        config = AppConfig.config()
        self.logLevel = config[AppConfig.LOG_LEVEL]
        self.config_path = self._get_config_path(config[AppConfig.CONFIGURATION_PATH])
        self._load_config()
        
    def _get_config_path(self, config_path):
        return Path(config_path) / LoggerConfig.CONFIG_FILE_NAME

    def _load_config(self):
        try:
            with open(self.config_path) as f:
                config_str = os.path.expandvars(f.read())
                config_str = config_str.replace(LoggerConfig.LOG_LEVEL_PLACEHOLDER, self.logLevel)
                config = yaml.safe_load(config_str)
                logging.config.dictConfig(config)
                logging.info(f"Loaded logging config from {self.config_path}")

        except FileNotFoundError:
            logging.basicConfig(level=self.logLevel)
            logging.warning(f"Using default logging config. Configuration file not found at {self.config_path}")

        except Exception as e:
            logging.basicConfig(level=self.logLevel)
            logging.error(f"Error loading logging config: {str(e)}")
            logging.error(traceback.format_exc())

    @staticmethod
    def get_logger(name: str = None):
        return logging.getLogger(name or __name__)