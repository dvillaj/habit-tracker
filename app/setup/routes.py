from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from app.database.models import User
from app.app_factory import db

setup_bp = Blueprint('setup', __name__)

@setup_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    # Verificar si ya existe algún usuario
    if User.query.count() > 0:
        flash('El sistema ya fue configurado previamente', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Todos los campos son requeridos', 'danger')
            return redirect(url_for('setup.setup'))
        
        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'danger')
            return redirect(url_for('setup.setup'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este email ya está registrado', 'danger')
            return redirect(url_for('setup.setup'))
        
        try:
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Configuración completada exitosamente. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error en la configuración: ' + str(e), 'danger')
    
    return render_template('setup.html')