from flask import Blueprint
from src.core.models.config_model import Config

api_state_bp = Blueprint("state_api", __name__, url_prefix="/api/state")

@api_state_bp.get("/")
def index():
    try:
        config = Config.get_singleton()

        info = {
            "enabled": config.state
        }

        if not config.state:
            info.update({
                "message": config.information
            })

        return info, 200
    except Exception as e:
        return {"error": "Internal server error", "details": str(e)}, 500