from flask import Blueprint
from flask import request
from src.core.models.user_model import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_access_token

api_auth_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")

@api_auth_bp.post("/")
def index():
    username = request.json.get('user', None)
    password = request.json.get('password', None)
    try:
        user = User.check_user(username, password)
        if not user:
            return {"error": "Usuario o contraseña incorrectos"}, 400
        if user.activo == False:
            return {"error": "Usuario deshabilitado, contacte al administrador"}, 403
        access_token = create_access_token(identity=username)
        return {"token": access_token}, 200
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500