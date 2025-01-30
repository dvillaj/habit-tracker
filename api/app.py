from flask import Flask, jsonify, request, redirect, url_for, render_template
from business_logic.habit_logic import Habit, get_all_habits, create_habit, get_habit_by_id, update_habit
from business_logic.database import init_db 
from config import DATABASE_PATH

app = Flask(__name__, template_folder='../templates')
app.config['DATABASE'] = DATABASE_PATH

# Inicializar la base de datos al iniciar la aplicación
with app.app_context():
    init_db()

# @app.route('/api/habits', methods=['GET'])
def get_habits():
    habits = get_all_habits()
    return jsonify([dict(habit) for habit in habits])

@app.route('/api/habits', methods=['POST'])
def add_habit():
    data = request.get_json()
    new_habit = Habit(data['name'], data['type'])
    create_habit(new_habit)
    return jsonify({'message': 'Habit created'}), 201

# Rutas para el frontend
@app.route('/')
def index():
    habits = get_all_habits()
    return render_template('index.html', habits=habits)

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
        update_habit(habit_id, request.form['name'], request.form['type'])
        return redirect(url_for('index'))
    
    return render_template('edit_habit.html', habit=habit)

# Nueva ruta API para edición
@app.route('/api/habits/<int:habit_id>', methods=['PUT'])
def api_update_habit(habit_id):
    data = request.get_json()
    update_habit(habit_id, data['name'], data['type'])
    return jsonify({'message': 'Habit updated'}), 200