import logging
import logging.config
import os
import yaml
from config.environment import LOG_LEVEL, CONFIGURATION_PATH
from pathlib import Path
import traceback

class LoggerConfig:
    
    CONFIG_FILE_NAME = "logging_config.yaml"
    LOG_LEVEL_PLACEHOLDER = "${LOG_LEVEL}"

    def __init__(self):
        self.config_path = self._get_config_path()
        self._load_config()
        
    def _get_config_path(self):
        return Path(CONFIGURATION_PATH) / LoggerConfig.CONFIG_FILE_NAME

    def _load_config(self):
        try:
            with open(self.config_path) as f:
                config_str = os.path.expandvars(f.read())
                config_str = config_str.replace(LoggerConfig.LOG_LEVEL_PLACEHOLDER, LOG_LEVEL)
                config = yaml.safe_load(config_str)
                logging.config.dictConfig(config)
                logging.info(f"Loaded logging config from {self.config_path}")
        except FileNotFoundError:
            logging.basicConfig(level=LOG_LEVEL)
            logging.warning(f"Using default logging config. Configuration file not found at {self.config_path}")
        except Exception as e:
            logging.basicConfig(level=LOG_LEVEL)
            logging.error(f"Error loading logging config: {str(e)}")
            logging.error(traceback.format_exc())

    @staticmethod
    def get_logger(name: str = None):
        return logging.getLogger(name or __name__)