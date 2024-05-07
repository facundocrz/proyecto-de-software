from flask import Blueprint
from flask import request
from src.core.models.service_model import Service
from src.core.models.config_model import Config
from src.core.models.type_model import Type
from src.web.schemas.service import services_schema, service_schema
from src.web.schemas.type import types_schema
from flask_jwt_extended import jwt_required
from src.web.api.helpers.validations import is_integer

api_service_bp = Blueprint("service_api", __name__, url_prefix="/api")

@api_service_bp.get("/services/search")
def search():
    try:
        q = request.args.get('q', None)
        
        if any(not (c.isalpha() or c.isdigit() or c.isspace()) for c in q):
            return {"error": "Parametro de busqueda invalido"}, 400
        type = request.args.get('type', None)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.get_singleton().cant))
        if not q:
            return {"error": "Invalid parameters"}, 400
        paginated_data = Service.get_all_active_paginated_by_search(q, type, page, per_page)
        services_as_dicts = services_schema.dump(paginated_data.items)
        for service_data in services_as_dicts:
            service = Service.get_service(service_data["id"])
            service_data["type_name"] = service.type.name
            service_data["institution_name"] = service.institution.name
        response = {
            "data": services_as_dicts,
            "page": paginated_data.page,
            "per_page": per_page,
            "total": paginated_data.total
        }
        
        return response, 200
    except ValueError:
        return {"error": "'page' and 'per_page' parameters must be integer numbers"}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 

@api_service_bp.get("/services/<int:service_id>")
def show(service_id):
    try:
        is_integer(service_id)
        service = Service.get_active_service_in_active_institution(service_id)
        if service:
            service_as_dict = service_schema.dump(service)
            service_as_dict["type_name"] = service.type.name
            service_as_dict["institution_name"] = service.institution.name
            return service_as_dict, 200
        return {"error": "Service not found"}, 400
    except ValueError as e:
        return {"error": "URL parameter must be an integer number"}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 

@api_service_bp.get("/services-types")
def types():
    try:
        types = Type.get_all_types()
        if types:
            types_as_dict = types_schema.dump(types)
            return {"data": types_as_dict}, 200
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500 