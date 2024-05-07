import json
import math
from flask import abort, Blueprint, redirect, render_template, request, url_for, session, flash
from flask_mail import Message
from src.core.models import crear_usuario
from src.core.models.user_model import User
from src.core.models.role_model import Role
from src.core.models.institution_model import Institution
from src.core.models.config_model import Config
from src.core.bcrypt import bcrypt
from src.web.mail import mail
from src.web.helpers.auth import login_required, has_permission
from src.web.helpers.validations import (
    validate_email,
    validate_username,
    validate_password,
    validate_first_name,
    validate_last_name,
    validate_active
)
from src.web.helpers.session import get_current_user
from src.web.helpers.tokens import get_serializer


user_blueprint = Blueprint("user", __name__, url_prefix="/user")

role_blueprint = Blueprint("role", __name__, url_prefix="/role")
user_blueprint.register_blueprint(role_blueprint)


@user_blueprint.get("/")
@user_blueprint.get("/<int:page>")
@login_required
@has_permission("user_index")
def index(page=1):
    page_size = Config.get_singleton().cant

    users, users_count = User.paginate(page, page_size, request.args.get("email"), request.args.get("filter"))
    page_count = math.ceil(users_count / page_size)

    return render_template(
        "user/index.html.jinja",
        users=users,
        users_count=users_count,
        page=page,
        page_count=page_count,
        filter_email=request.args.get("email", ""),
        filter_active=request.args.get("filter", "")
    )


def create_update(user=None, arglist=None):
    form = request.form

    if isinstance(user, int):
        user = User.get(user)

    args = {
        'email': validate_email,
        'username': validate_username,
        'password': validate_password,
        'first_name': validate_first_name,
        'last_name': validate_last_name,
        'activo': validate_active
    }

    kwargs = {}
    for key, fn in args.items():
        if arglist and key not in arglist:
            continue
        value, *err = fn(form, user)
        if value is None:
            if len(err) > 0:
                flash(err[0], "danger")
            break
        kwargs[key] = value
    else:
        if user:
            if user.has_role(Role.get_by_name("Super Administrador")) and args['activo'](form, user)[0] == False:
                flash("No se puede deshabilitar el usuario superadministrador", "danger")
                return None
            user.update(**kwargs)
        else:
            user = crear_usuario(**kwargs)
        return user
        
    return None


@user_blueprint.post("/create")
@login_required
@has_permission("user_create")
def create():
    if create_update():
        flash("¡Se creó el usuario de manera exitosa!", "success")
    
    return redirect(url_for("user.index"))


@user_blueprint.post("/update/<int:userid>")
@login_required
@has_permission("user_update")
def update(userid):
    arglist = ['email', 'username', 'first_name', 'last_name', 'activo']
    if request.form.get('change_password'):
        arglist.append('password')
        
    if create_update(userid, arglist):
        flash("¡Se actualizó el usuario de manera exitosa!", "success")
    
    return redirect(url_for("user.index"))


@user_blueprint.post("/delete/<int:userid>")
@login_required
@has_permission("user_destroy")
def delete(userid):
    user = User.get(userid)
    if user:
        if user.has_role(Role.get_by_name("Super Administrador")):
            flash("No se puede eliminar el usuario superadministrador", "danger")
        else:
            user.delete()
    else:
        flash(f"No se pudo eliminar el usuario con ID: {userid}")
    
    return redirect(url_for("user.index"))


@role_blueprint.get("/<int:userid>", endpoint="index")
@login_required
@has_permission("user_index")
def role_index(userid):
    user = User.get(userid)
    if not user:
        abort(404)
    
    roles = Role.get_all()
    insts = Institution.get_all()

    user_roles = []
    for ur in user.get_roles():
        user_roles.append({
            "role": Role.find_by_id(ur.role_id),
            "inst": Institution.find_by_id(ur.institution_id),
            "id": f"r{ur.role_id}-i{ur.institution_id or 0}"
        })
    
    user_roles_count = len(user_roles)
    
    return render_template(
        "user/roles.html.jinja",
        user=user,
        roles=roles,
        insts=insts,
        user_roles=user_roles,
        user_roles_count=user_roles_count
    )


@role_blueprint.post("/<int:userid>/add", endpoint="add")
@login_required
@has_permission("user_update")
def role_add(userid):
    user = User.get(userid)
    if not user:
        abort(404)
    
    roleid = request.form.get("roleid")
    role = Role.find_by_id(roleid) if roleid else None
    if not role:
        abort(404)
    
    if role.name == "Super Administrador":
        abort(404)
    
    instid = request.form.get("instid")
    inst = Institution.find_by_id(instid) if instid else None
    if not inst:
        abort(404)
    
    if user.has_role(role, inst):
        flash("Ya existe un rol similar para el usuario", "danger")
    else:
        user.add_role(role, inst)
        
    return redirect(url_for("user.role.index", userid=user.id))


@role_blueprint.post("/<int:userid>/remove/<int:roleid>", endpoint="remove")
@role_blueprint.post("/<int:userid>/remove/<int:roleid>/<int:instid>", endpoint="remove")
@login_required
@has_permission("user_update")
def role_remove(userid, roleid, instid=None):
    user = User.get(userid)
    if not user:
        abort(404)

    role = Role.find_by_id(roleid)
    if not role:
        abort(404)
    
    if role.name == "Super Administrador":
        abort(404)

    if instid:
        inst = Institution.find_by_id(instid)
        if not inst:
            abort(404)
    else:
        inst = None

    ok = user.remove_role(role, inst)
    if not ok:
        flash("No se pudo eliminar el rol", "danger")
    
    return redirect(url_for("user.role.index", userid=user.id))


@user_blueprint.route("/register", methods=["GET", "POST"])  
def register():
    if request.method == 'POST':
        user = create_update(arglist=['email', 'first_name', 'last_name'])
        if user:
            ser = get_serializer("confirmation")
            tok = ser.dumps({"user_id": user.id})

            msg = Message(
                "Confirmación de usuario",
                recipients=[user.email]
            )
            msg.html = render_template('email.html.jinja', token=tok)
            mail.send(msg)

            flash(
                "Le enviamos un enlace de confirmación a su casilla de correo electrónico. "
                "Por favor, confirme su correo antes de iniciar sesión.",
                "warning"
            )

            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("user.register"))
    elif request.method == 'GET':
        return render_template('register_user.html.jinja')


@user_blueprint.route("/confirm/<token>", methods=["GET", "POST"])
def confirm(token):
    try:
        ser = get_serializer("confirmation")
        data = ser.loads(token)
    except:
        abort(404)
    
    user_id = data.get('user_id')
    if user_id is None:
        abort(404)

    user = User.find_by_id(data['user_id'])
    if user is None:
        abort(404)
    
    if user.exists:
        abort(404)
    
    if request.method == 'POST':
        if create_update(user=user, arglist=['username', 'password']):
            flash("¡Su usuario ha sido confirmado exitosamente!", "success")
            return redirect(url_for("auth.login"))

    return render_template("user/confirm.html.jinja", token=token, user=user)


@user_blueprint.route("/profile", methods=["GET", "POST"]) 
@login_required  
def profile():
    user = get_current_user()
    if not user:
        abort(404)

    if request.method == "POST":
        arglist = ['username', 'first_name', 'last_name']
        if request.form.get('change_password'):
            arglist.append('password')
            
        if create_update(user=user, arglist=arglist):
            flash("¡Se actualizaron sus datos de manera exitosa!", "success")
    
    return render_template('user/profile.html.jinja', user=user)
