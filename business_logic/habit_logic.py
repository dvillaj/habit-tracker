from .database import get_db_connection
import sqlite3

class Habit:
    def __init__(self, name, habit_type):
        self.name = name
        self.type = habit_type

def get_all_habits():
    conn = get_db_connection()
    habits = conn.execute('SELECT * FROM habits').fetchall()
    conn.close()
    return habits

def create_habit(habit):
    conn = get_db_connection()
    conn.execute('INSERT INTO habits (name, type) VALUES (?, ?)',
               (habit.name, habit.type))
    conn.commit()
    conn.close()

def get_habit_by_id(habit_id):
    conn = get_db_connection()
    habit = conn.execute('SELECT * FROM habits WHERE id = ?', (habit_id,)).fetchone()
    conn.close()
    return habit

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

    except sqlite3.IntegrityError:
        # Avoid duplicate logs for the same day
        pass

    finally:
        conn.close()

        

def get_habits_with_logs():
    conn = get_db_connection()
    habits = conn.execute('''
        SELECT habits.*, 
               COUNT(logs.id) as log_count,
               GROUP_CONCAT(logs.date, ', ') as log_dates,
               MAX(logs.date) as last_logged
        FROM habits
        LEFT JOIN logs ON habits.id = logs.habit_id
        GROUP BY habits.id
    ''').fetchall()
    conn.close()
    return habits