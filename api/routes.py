from flask import request, redirect, url_for, render_template, flash, abort, jsonify
from business_logic.habit_logic import *
from datetime import datetime, date
from calendar import month_name

logger = LoggerConfig.get_logger(__name__)

def register_routes(app):

    # Rutas para el frontend
    @app.route('/')
    def index():
        habits = get_all_habits()
        return render_template('index.html', habits=habits, date=date)

    @app.route('/create', methods=['GET', 'POST'])
    def create_habit_endpoint():
        if request.method == 'POST':
            name = request.form['name']
            habit = Habit(name, request.form['type'])
            try:
                create_habit(habit)
                flash(f"Habit '{name}' created successfully!", 'success')

            except sqlite3.IntegrityError:
                flash(f"⚠️ Habit '{name}' already exists", 'warning')

            return redirect(url_for('index'))

        return render_template('create_habit.html')

    # Añadir estas nuevas rutas
    @app.route('/edit/<int:habit_id>', methods=['GET', 'POST'])
    def edit_habit_endpoint(habit_id):
        habit = get_habit_by_id(habit_id)
        
        if not habit:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            name= request.form['name']
            type = request.form['type']

            try:
                update_habit(habit_id, name, type)
                flash('Habit updated successfully!', 'success')

            except sqlite3.IntegrityError:
                flash(f"⚠️ Habit '{name}' already exists", 'warning')

            return redirect(url_for('index'))
        
        return render_template('edit_habit.html', habit=habit)


    @app.route('/log/<int:habit_id>', methods=['POST'])
    def log_habit_endpoint(habit_id):
        log_date = request.form.get('date', str(date.today()))
        
        success = create_log(habit_id, log_date)
        
        if success:
            flash('✅ Habit logged successfully!', 'success')
        else:
            flash('⚠️ This habit was already logged for selected date', 'warning')
        
        return redirect(url_for('index'))


    @app.route('/habits/<int:habit_id>/delete', methods=['POST'])
    def delete_habit_endpoint(habit_id):
        try:
            if delete_habit(habit_id):
                flash('✅ Habit deleted successfully!', 'success')
            else:
                flash('⚠️ Error deleting habit', 'error')
        except Exception as e:
            flash(f'🚨 Error: {str(e)}', 'danger')

        return redirect(url_for('index'))



    @app.route('/habits/<int:habit_id>/stats')
    def habit_stats_endpoint(habit_id):
        year = request.args.get('year', date.today().year, type=int)
        month = request.args.get('month', date.today().month, type=int)
        
        stats = get_habit_stats(habit_id)
        
        if not stats:
            abort(404)
        
        # Generar calendario
        cal = calendar.Calendar()
        month_days = cal.monthdatescalendar(year, month)

        
        prev_year, prev_month = (year, month-1) if month > 1 else (year-1, 12)
        next_year, next_month = (year, month+1) if month < 12 else (year+1, 1)
        
        return render_template('stat_habit.html',
                            stats=stats,
                            month_days=month_days,
                            current_date=date.today(),
                            prev_year=prev_year,
                            prev_month=prev_month,
                            next_year=next_year,
                            next_month=next_month,
                            year=year,
                            month=month)


    @app.route('/toggle_log', methods=['POST'])
    def toggle_log_endpoint():
        habit_id = request.form['habit_id']
        log_date = request.form['log_date']
        year = request.form['year']
        month = request.form['month']
        
        try:
            # Validar fecha
            selected_date = date.fromisoformat(log_date)
            if selected_date > date.today():
                raise ValueError("Cannot log future dates")
                
            action = toggle_log(habit_id, log_date)
            flash(f'Log {action} successfully!', 'success')

        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        
        return redirect(url_for('habit_stats_endpoint', 
                            habit_id=habit_id, 
                            year=year, 
                            month=month))

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
        

    @app.route('/health')
    def health_check():
        logger.debug("Health check")
        return jsonify(status="healthy"), 200


    @app.context_processor
    def utility_processor():
        import calendar

        return {
            'month_name': month_name,
            'get_prev_next': lambda y, m: (
                (y, m-1) if m > 1 else (y-1, 12),
                (y, m+1) if m < 12 else (y+1, 1)
            )
        }    

