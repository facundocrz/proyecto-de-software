import math
from flask import abort, Blueprint, redirect, render_template, request, url_for, session, flash
from src.core.models import create_institution
from src.core.models.institution_model import Institution
from src.core.models.role_model import Role
from src.core.models.user_model import User
from src.core.models.config_model import Config
from src.web.helpers.auth import login_required, has_permission, check_permission
from src.web.helpers.session import get_current_user, get_current_institution


role_blueprint = Blueprint("role", __name__, url_prefix="/role")


@role_blueprint.get("/", endpoint="index")
@role_blueprint.get("/<int:page>", endpoint="index")
@has_permission("role_index")
def role_index(page=1):
    inst = get_current_institution()
    if not inst:
        abort(404)

    page_size = Config.get_singleton().cant
    
    urlist_raw, urlist_count = inst.get_user_roles(page, page_size)
    page_count = math.ceil(urlist_count / page_size)

    urlist = []
    for ur in urlist_raw:
        urlist.append({
            "role": Role.get_by_id(ur.role_id),
            "user": User.get(ur.user_id),
            "id": f"r{ur.role_id}-u{ur.user_id}"
        })
    
    roles = Role.get_all()

    return render_template(
        "role/index.html.jinja",
        inst=inst,
        urlist=urlist,
        urlist_count=urlist_count,
        page=page,
        page_count=page_count,
        roles=roles
    )


@role_blueprint.post("/add", endpoint="add")
@has_permission("role_create")
def role_add():
    inst = get_current_institution()
    if not inst:
        abort(404)

    role_id = request.form.get("role_id")
    role = Role.get_by_id(role_id) if role_id else None
    if not role:
        abort(404)

    user_email = request.form.get("user_email")
    user = User.find_user_by_email(user_email) if user_email else None
    if user and user.activo:
        if user.has_role(role, inst):
            flash(f'El usuario "{user.username}" ya tiene el rol "{role.name}".', "danger")
        else:
            user.add_role(role, inst)
    else:
        flash("No se pudo encontrar un usuario con el email ingresado.", "danger")

    return redirect(url_for("role.index"))


@role_blueprint.post("/remove/<int:roleid>/<int:userid>", endpoint="remove")
@has_permission("role_destroy")
def role_remove(roleid, userid):
    role = Role.get_by_id(roleid)
    if not role:
        abort(404)

    inst = get_current_institution()
    if not inst:
        abort(404)
    
    user = User.get(userid)
    if not user:
        abort(404)
    
    user.remove_role(role, inst)

    return redirect(url_for("role.index"))