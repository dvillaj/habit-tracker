from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.database.models import Habit, ExampleHabit
from app.app_factory import db
from werkzeug.utils import secure_filename
from app.utils.file_uploads import allowed_file
import os

habits_bp = Blueprint('habits', __name__, template_folder='templates')

@habits_bp.route('/', methods=['GET']) 
@login_required
def list_habits():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template('habits/list.html', habits=habits)

@habits_bp.route('/habits/create', methods=['GET', 'POST'])
@login_required
def create_habit():
    
    examples = ExampleHabit.query.all()

    if request.method == 'POST':
        try:
            
            title = request.form['title'].strip()
            
            # Validar nombre único
            existing = Habit.query.filter_by(
                user_id=current_user.id,
                title=title
            ).first()
            
            if existing:
                flash('Ya tienes un hábito con este nombre', 'danger')
                return render_template('habits/create.html', examples=examples)
            
            # Manejar la subida del icono
            icon_filename = None
            if 'icon' in request.files:
                icon_file = request.files['icon']
                if icon_file and allowed_file(icon_file.filename):
                    filename = secure_filename(icon_file.filename)
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    
                    # Crear directorio si no existe
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    # Guardar archivo
                    filepath = os.path.join(upload_folder, filename)
                    icon_file.save(filepath)
                    icon_filename = filename

            # Crear el hábito
            new_habit = Habit(
                title=request.form['title'],
                description=request.form.get('description', ''),
                days=','.join(request.form.getlist('days')),
                icon=icon_filename,
                user_id=current_user.id
            )
            
            db.session.add(new_habit)
            db.session.commit()
            flash('Hábito creado exitosamente', 'success')
            return redirect(url_for('habits.list_habits'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creando hábito: {str(e)}', 'danger')
    
    return render_template('habits/create.html', examples=examples)