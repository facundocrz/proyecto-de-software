from flask import Blueprint
from flask import request
from src.core.models.config_model import Config

api_contact_bp = Blueprint("contact_api", __name__, url_prefix="/api/contact")

@api_contact_bp.get("/")
def index():
    try:
        config = Config.find_by_id(1)
        contact_info_as_dict = {
            "cant": config.cant,
            "phone": config.contact,
            "email": config.email
        }

        return contact_info_as_dict, 200
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500