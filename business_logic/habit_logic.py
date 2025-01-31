from .database import get_db_connection
import sqlite3
from config.logger_config import LoggerConfig

logger = LoggerConfig.get_logger(__name__)

class Habit:
    def __init__(self, name, habit_type, id =0, log_count=0, log_dates = [], last_logged=None):
        self.id = id
        self.name = name
        self.type = habit_type
        self.log_count = log_count
        self.log_dates = log_dates
        self.last_logged = last_logged

def get_all_habits():
    conn = get_db_connection()
    habits = conn.execute('''
        SELECT 
            habits.id,
            habits.name,
            habits.type,
            COUNT(logs.id) as log_count,
            GROUP_CONCAT(logs.date, ', ') as log_dates,
            MAX(logs.date) as last_logged
        FROM habits
        LEFT JOIN logs ON habits.id = logs.habit_id
        GROUP BY habits.id
    ''').fetchall()
    conn.close()
    return [Habit(h['name'], h['type'], h['id'], h['log_count'], h['log_dates'], h['last_logged']) for h in habits]

def create_habit(habit):
    logger.info(f"Creating habit {habit.name}")

    conn = get_db_connection()
    conn.execute('INSERT INTO habits (name, type) VALUES (?, ?)',
               (habit.name, habit.type))
    conn.commit()
    conn.close()

def get_habit_by_id(habit_id):
    conn = get_db_connection()
    habit = conn.execute('SELECT * FROM habits WHERE id = ?', (habit_id,)).fetchone()
    conn.close()
    return Habit(habit['name'], habit['type'])


def update_habit(habit_id, name, habit_type):
    conn = get_db_connection()
    conn.execute('UPDATE habits SET name = ?, type = ? WHERE id = ?',
               (name, habit_type, habit_id))
    conn.commit()
    conn.close()    

def create_log(habit_id, date):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO logs (habit_id, date) VALUES (?, ?)', 
                   (habit_id, date))
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # Avoid duplicate logs for the same day
        return False

    finally:
        conn.close()


def delete_habit(habit_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM logs WHERE habit_id = ?', (habit_id,))
        conn.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting habit: {str(e)}")
        conn.rollback()
        raise e
    finally:
        conn.close()

