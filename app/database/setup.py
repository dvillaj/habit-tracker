from app.app_factory import db
from app.database.models import ExampleHabit


def create_initial_data():
    if ExampleHabit.query.count() == 0:
        examples = [
            ExampleHabit(title="Ejercicio", description="30 minutos de actividad física", icon="exercise.svg"),
            ExampleHabit(title="Leer", description="20 páginas diarias", icon="book.svg"),
            ExampleHabit(title="Meditar", description="10 minutos de meditación", icon="meditation.svg")
        ]
        db.session.bulk_save_objects(examples)
        db.session.commit()