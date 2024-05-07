from flask import Blueprint
from flask import request
from src.core.models.institution_model import Institution
from src.core.models.config_model import Config
from src.web.schemas.institution import institutions_schema, institution_schema

api_institution_bp = Blueprint("institution_api", __name__, url_prefix="/api/institutions")

@api_institution_bp.get("/")
def index():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.get_singleton().cant))
        paginated_data = Institution.get_all_active_paginated(page, per_page)
        institutions = paginated_data.items
        
        institutions_as_dicts = institutions_schema.dump(institutions)
        
        response = {
            "data": institutions_as_dicts,
            "page": paginated_data.page,
            "per_page": paginated_data.per_page,
            "total": paginated_data.total
        }
        
        return response, 200
    except ValueError:
        return {"error": "'page' and 'per_page' parameters must be integer numbers"}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500

@api_institution_bp.get("/<int:inst_id>")
def show(inst_id):
    try:
        inst = Institution.find_by_id(inst_id)
        if inst:
            inst_as_dict = institution_schema.dump(inst)
            return inst_as_dict, 200
        else:
            return {"error": "Institution not found"}, 400
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500