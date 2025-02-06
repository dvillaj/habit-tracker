from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.database.models import Habit, ExampleHabit
from app.app_factory import db
from app.utils.file_uploads import allowed_file, save_icon
import os
from config.logger import LoggerConfig

habits_bp = Blueprint('habits', __name__, template_folder='templates')
logger = LoggerConfig.get_logger(__name__)

@habits_bp.route('/', methods=['GET']) 
@login_required
def list_habits():
    logger.info("Listing habits ...")
    current_app.logger.info("Listing habits ...")
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template('habits/list.html', habits=habits)

@habits_bp.route('/habits/create', methods=['GET', 'POST'])
@login_required
def create_habit():
    
    examples = ExampleHabit.query.all()

    if request.method == 'POST':
        try:
                  
            form_data = {
                'title': request.form.get('title', ''),
                'description': request.form.get('description', ''),
            }
            
            title = form_data['title'].strip()
            if not title:
                raise ValueError("El título es requerido")
                        
            # Validar nombre único
            existing = Habit.query.filter_by(
                user_id=current_user.id,
                title=title
            ).first()
            
            if existing:
                flash('Ya tienes un hábito con este nombre', 'danger')
                return render_template('habits/create.html', examples=examples, form=form_data)
            
            # Manejar la subida del icono
            icon_filename = None
            if 'icon' in request.files:
                icon_file = request.files['icon']
                if icon_file and allowed_file(icon_file.filename):
                    icon_filename = save_icon(icon_file)

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
