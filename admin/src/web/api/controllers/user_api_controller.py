from flask import Blueprint
from flask import request
from src.core.models.request_model import Request
from src.core.models.user_model import User
from src.core.models.service_model import Service
from src.core.models.config_model import Config
from src.web.schemas.user import user_schema
from src.web.schemas.request import requests_schema
from src.web.schemas.request import request_schema
from src.web.schemas.request import CreateRequestSchema
from src.web.schemas.comment import CreateCommentSchema
from src.core.models import create_request
from src.core.models import create_comment
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from src.web.api.helpers.validations import is_integer
from sqlalchemy.exc import IntegrityError

api_user_bp = Blueprint("user_api", __name__, url_prefix="/api/me")

@api_user_bp.get("/profile")
@jwt_required()
def profile():
    try:
        user = User.find_user(get_jwt_identity())
        user_as_dict = user_schema.dump(user)
        return user_as_dict, 200
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 


@api_user_bp.get("/requests")
@jwt_required()
def get_requests():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.get_singleton().cant))
        sort = request.args.get('sort', None)
        order = request.args.get('order', 'asc')
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        filter = request.args.get('filter', 'All')
        if sort:
            if sort not in ["id","title", "created_at", "updated_at", "current_status"]:
                return {"error": "'sort' parameter must be 'id','title', 'created_at', 'updated_at' or 'status'."}, 400
        if order:
            if order not in ['asc', 'desc']:
                return {"error": "'order' parameter must be 'asc' or 'desc'."}, 400
        if filter:
            if filter not in ['All', 'Creada', 'Aceptada', 'En proceso', 'Rechazada', 'Cancelada', 'Finalizada']:
                return {"error": "'filter' parameter must be 'all', 'Creada', 'Aceptada', 'En proceso', 'Rechazada', 'Cancelada' or 'Finalizada'."}, 400        
        user = User.find_user(get_jwt_identity())
        paginated_data = Request.get_all_paginated_by_user(user,page, per_page, sort, order, start_date, end_date, filter)
        requests_as_dicts = requests_schema.dump(paginated_data.items)
        response = {
            "data": requests_as_dicts,
            "page": paginated_data.page,
            "per_page": per_page,
            "total": paginated_data.total
        }
        return response, 200
    except ValueError:
        return {"error": "'page' and 'per_page' parameters must be integer numbers"}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 


@api_user_bp.get("/requests/<request_id>")
@jwt_required()
def get_request(request_id):
    try:
        is_integer(request_id)
        user = User.find_user(get_jwt_identity())
        request = Request.query.filter_by(id=request_id, user_id=user.id).first()
        if request:
            request_as_dict = request_schema.dump(request)
            for comment in request_as_dict["comments"]:
                comment["username"] = User.get_username_by_id(comment["user_id"])
            request_as_dict["institution"] = request.service.institution.name
            return request_as_dict, 200
        return {"error": "Request not found"}, 400
    except ValueError as e:
        return {"error": "URL parameter must be an integer number"}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 


@api_user_bp.post("/requests")
@jwt_required()
def create_new_request():
    try:
        user = User.find_user(get_jwt_identity())
        schema = CreateRequestSchema()
        data = schema.load(request.json)
        errors = schema.validate(data)
        service = Service.find_by_id(data['service_id'])
        if not service or not service.habilite:
            return {"error": "Service not found"}, 400
        new_request = create_request(user_id = user.id, title=data['title'].strip(), description = data['description'].strip(), service_id=data['service_id'])
        request_as_dict = request_schema.dump(new_request)
        return request_as_dict, 201
    except ValidationError as e:
        # Maneja errores de validación generados por Marshmallow
        return {"error": "Invalid parameters", "errors": e.messages}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 


@api_user_bp.post("/requests/<int:request_id>/notes")
@jwt_required()
def create_request_note(request_id):
    try:
        is_integer(request_id)
        user = User.find_user(get_jwt_identity())
        user_request = Request.query.filter_by(id=request_id, user_id=user.id).first()
        schema = CreateCommentSchema()
        data = schema.load(request.json)
        errors = schema.validate(data)
        if request:
            comment = create_comment(content=data["text"].strip(), request_id=request_id, user_id=user.id)
            request_as_dict = request_schema.dump(user_request)
            return request_as_dict, 201
        return {"error": "Request not found"}, 400
    except ValidationError as e:
        return {"error": "Invalid parameters", "errors": e.messages}, 400
    except IntegrityError:
        return {"error": "Failed to create a comment"}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 