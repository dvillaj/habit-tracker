from config import Config
import uuid
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_icon(icon_file):
    if icon_file and allowed_file(icon_file.filename):
        # Generar nombre único
        ext = icon_file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        # Guardar archivo
        icon_file.save(filepath)
        return filename
    return None
