import sqlite3
from config.app_config import AppConfig

def get_db_connection():
    config = AppConfig.config()
    conn = sqlite3.connect(config[AppConfig.DATABASE_PATH])
    conn.row_factory = sqlite3.Row
    return conn

def init_db(config):
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS habits
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  type TEXT CHECK(type IN ('positive', 'negative')) NOT NULL)''')
                  
    conn.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_habits_unique_name
                    ON habits ( name)''')
    
    # Modificar la tabla logs
    conn.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  habit_id INTEGER NOT NULL,
                  date DATE NOT NULL DEFAULT CURRENT_DATE,
                  UNIQUE(habit_id, date),
                  FOREIGN KEY(habit_id) REFERENCES habits(id))''')

    conn.commit()
    conn.close()
