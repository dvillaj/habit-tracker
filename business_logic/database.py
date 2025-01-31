import sqlite3
from config.environment import DATABASE_PATH
import os

def get_db_connection():
    db_directory = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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
