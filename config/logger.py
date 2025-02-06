import logging.config
import yaml
from pathlib import Path
from .settings import Config
import logging

class LoggerConfig:
    _configured = False

    @classmethod
    def configure(cls):
        if not cls._configured:      
            config_path = Path(__file__).parent.parent / 'logging_config.yaml'            
            with open(config_path) as f:
                config_str = f.read().replace('${LOG_LEVEL}', Config.LOG_LEVEL)
                config = yaml.safe_load(config_str)
                
            logging.config.dictConfig(config)
            logging.debug("Logging setup sucessfully")
            cls._configured = True

    @classmethod
    def get_logger(cls, name='app'):
        if not cls._configured:
            cls.configure()
        return logging.getLogger(name)