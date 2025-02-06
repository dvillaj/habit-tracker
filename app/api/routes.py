from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.database.models import Habit, User

api_bp = Blueprint('api', __name__)

@api_bp.route('/habits', methods=['GET'])
@jwt_required()
def get_habits():
    current_user_id = get_jwt_identity() 
    habits = Habit.query.filter_by(user_id=current_user_id).all()
    return jsonify([habit.to_dict() for habit in habits]), 200


@api_bp.route('/login', methods=['POST'])
def api_login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            response = jsonify({"error": "Credenciales inválidas"})
            return make_response(response, 401, {'Content-Type': 'application/json; charset=utf-8'})
        
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@api_bp.route('/health')
def health_check():
    return jsonify(status="healthy"), 200    