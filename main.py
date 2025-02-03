import os
from dotenv import load_dotenv
from api.app import create_app
from config.logger_config import LoggerConfig
from config.app_config import AppConfig
import traceback

# Load environment variables
load_dotenv()

# Load configuration
config = AppConfig.config()

# Init logger
LoggerConfig()
logger = LoggerConfig.get_logger(__name__)

def initialize_application():
    config = AppConfig.config()

    # Create the database directory if it doesn't exist
    os.makedirs(os.path.dirname(config[AppConfig.DATABASE_PATH]), exist_ok=True)
    
    # Create the Flask app
    app = create_app(config)
    
    # Initialize the database
    with app.app_context():
        from business_logic.database import init_db
        init_db(config)
    
    return app 

if __name__ == '__main__':

    try: 
        logger.info("Starting app")

        app = initialize_application()
        
        # Execute the app
        app.run(host=config[AppConfig.FLASK_HOST], 
                port=config[AppConfig.FLASK_PORT],
                debug=config[AppConfig.FLASK_DEBUG] == '1')
        
    except Exception as e:
        logger.error(f"Error starting app: {str(e)}")
        logger.error(traceback.format_exc())