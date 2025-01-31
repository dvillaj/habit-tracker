from .database import get_db_connection
import sqlite3
from config.logger_config import LoggerConfig
from datetime import date, timedelta

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


from datetime import date, timedelta
import calendar

def get_habit_stats(habit_id):
    conn = get_db_connection()
    habit = conn.execute('SELECT * FROM habits WHERE id = ?', (habit_id,)).fetchone()
    
    if not habit:
        return None
    
    logs = conn.execute('SELECT date FROM logs WHERE habit_id = ?', (habit_id,)).fetchall()
    log_dates = {row['date'] for row in logs}
    
    # Calcular streaks
    current_streak = calculate_streak(log_dates, habit['type'])
    max_streak = calculate_max_streak(log_dates, habit['type'])
    
    return {
        'habit': dict(habit),
        'total_logs': len(log_dates),
        'current_streak': current_streak,
        'max_streak': max_streak,
        'log_dates': log_dates
    }

def calculate_streak(log_dates, habit_type):
    streak = 0
    current_date = date.today()
    
    while True:
        date_str = current_date.isoformat()
        has_log = date_str in log_dates
        
        if (habit_type == 'positive' and has_log) or (habit_type == 'negative' and not has_log):
            streak += 1
        else:
            break
            
        current_date -= timedelta(days=1)
        
    return streak


def calculate_max_streak(log_dates, habit_type):
    # Convertir strings de fecha a objetos date y ordenar
    dates = sorted([date.fromisoformat(d) for d in log_dates])
    
    if not dates:
        return 0
    
    # Determinar rango de fechas a verificar
    start_date = dates[0]
    end_date = date.today() if habit_type == 'negative' else dates[-1]
    
    current_streak = 0
    max_streak = 0
    current_date = start_date
    last_logged = start_date
    
    # Convertir a set para búsquedas rápidas
    logged_dates = set(dates)
    
    while current_date <= end_date:
        is_logged = current_date in logged_dates
        
        # Lógica para diferentes tipos de hábitos
        if (habit_type == 'positive' and is_logged) or \
           (habit_type == 'negative' and not is_logged):
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
        
        # Manejar huecos en los logs para hábitos positivos
        if habit_type == 'positive' and is_logged:
            days_since_last = (current_date - last_logged).days
            if days_since_last > 1:
                current_streak = 1  # Reiniciar streak
            last_logged = current_date
        
        current_date += timedelta(days=1)
    
    # Caso especial para hábitos negativos
    if habit_type == 'negative':
        # Calcular días desde el último log hasta hoy
        last_log = max(log_dates) if log_dates else start_date
        last_log_date = date.fromisoformat(last_log)
        days_since_last = (date.today() - last_log_date).days
        current_streak = days_since_last
        max_streak = max(max_streak, current_streak)
    
    return max_streak


def toggle_log(habit_id, log_date):
    conn = get_db_connection()
    try:
        # Verificar si existe
        exists = conn.execute(
            'SELECT 1 FROM logs WHERE habit_id = ? AND date = ?',
            (habit_id, log_date)
        ).fetchone()

        if exists:
            conn.execute(
                'DELETE FROM logs WHERE habit_id = ? AND date = ?',
                (habit_id, log_date)
            )
            action = 'deleted'
        else:
            conn.execute(
                'INSERT INTO logs (habit_id, date) VALUES (?, ?)',
                (habit_id, log_date)
            )
            action = 'created'
        
        conn.commit()
        return action
    finally:
        conn.close()