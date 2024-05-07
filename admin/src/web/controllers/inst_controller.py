from flask import Blueprint, redirect, session, url_for
from src.core.models.institution_model import Institution


inst_blueprint = Blueprint("inst", __name__, url_prefix="/inst")


@inst_blueprint.get("/change/<int:instid>")
def change(instid):
    inst = Institution.find_by_id(instid)
    if inst and inst.activo:
        session["inst_id"] = inst.id
    else:
        abort(404)
    
    return redirect(url_for("home"))