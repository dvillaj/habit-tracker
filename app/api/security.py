from flask_jwt_extended import JWTManager, verify_jwt_in_request
from functools import wraps

jwt = JWTManager()

def init_jwt(app):
    jwt.init_app(app)

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            # Add your custom admin check here
            return fn(*args, **kwargs)
        return decorator
    return wrapper