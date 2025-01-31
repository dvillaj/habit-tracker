from flask import Flask, jsonify, request, redirect, url_for, render_template
from business_logic.habit_logic import *
from business_logic.database import init_db 
from config.environment import DATABASE_PATH, FLASK_SECRET_KEY
from flask import Flask, flash 
from datetime import date
from datetime import datetime
from config.logger_config import LoggerConfig

# Init logger
LoggerConfig()

logger = LoggerConfig.get_logger(__name__)
logger.info("Starting Flask app")

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['DATABASE'] = DATABASE_PATH

# Inicializar la base de datos al iniciar la aplicación
with app.app_context():
    init_db()

# Rutas para el frontend
@app.route('/')
def index():
    habits = get_all_habits()
    return render_template('index.html', habits=habits, date=date)

@app.route('/create', methods=['GET', 'POST'])
def create_habit_page():
    if request.method == 'POST':
        habit = Habit(
            request.form['name'],
            request.form['type']
        )
        create_habit(habit)
        return redirect(url_for('index'))

    return render_template('create_habit.html')

# Añadir estas nuevas rutas
@app.route('/edit/<int:habit_id>', methods=['GET', 'POST'])
def edit_habit(habit_id):
    habit = get_habit_by_id(habit_id)
    
    if not habit:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name= request.form['name']
        type = request.form['type']

        update_habit(habit_id, name, type)
        return redirect(url_for('index'))
    
    return render_template('edit_habit.html', habit=habit)


@app.route('/log/<int:habit_id>', methods=['POST'])
def log_habit(habit_id):
    log_date = request.form.get('date', str(date.today()))
    
    success = create_log(habit_id, log_date)
    
    if success:
        flash('✅ Habit logged successfully!', 'success')
    else:
        flash('⚠️ This habit was already logged for selected date', 'warning')
    
    return redirect(url_for('index'))


@app.template_filter('date_format')
def format_date(value):
    try:
        # Si el valor viene de SQLite como string
        if isinstance(value, str):
            date_obj = datetime.strptime(value, "%Y-%m-%d")
        else:
            date_obj = value
            
        return date_obj.strftime("%b %d, %Y")
    except:
        return "Invalid date"