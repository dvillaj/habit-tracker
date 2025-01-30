from .database import get_db_connection

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