from flask import Blueprint,redirect, render_template, request, url_for, session, flash
from src.core.google import google
from src.core.models.user_model import User
from src.core.models import crear_usuario
from src.web.helpers.validations import (
    validate_username,
    validate_password,
)

google_auth_blueprint = Blueprint("google_auth", __name__, url_prefix="/google")

@google_auth_blueprint.get("/auth")
def login_google():
    return google.authorize(callback=url_for('google_auth.authorized', _external=True))

@google_auth_blueprint.get("/authorized")
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    me = google.get('userinfo')
    user = User.find_user_by_email(me.data['email'])
    if user is None:
        session['google_user_info'] = {
            'email': me.data['email'],
            'given_name': me.data['given_name'],
            'family_name': me.data['family_name'],
        }
        return redirect(url_for("google_auth.complete_registration"))
    if user.activo:
            session['user_id'] = user.id
            return redirect(url_for("home"))
    else:
        flash("El usuario se encuentra desactivado", "danger")
        return redirect(url_for("home"))

@google_auth_blueprint.get("/complete_registration")
def complete_registration():
    google_user_info = session.get('google_user_info')
    if google_user_info is None:
        flash("Error: No se encontró información de usuario de Google.", "danger")
        return redirect(url_for("home"))
    return render_template("complete_registration.html.jinja", user_info=google_user_info)
    
@google_auth_blueprint.post("/complete_registration")
def complete_registration_post():
    google_user_info = session.get('google_user_info')
    if google_user_info is None:
        flash("Error: No se encontró información de usuario de Google.", "danger")
        return redirect(url_for("home"))

    form = request.form
    args = {
        'username': validate_username,
        'password': validate_password,
    }

    user = None
    kwargs = {}

    for key, fn in args.items():
        value, *err = fn(form, user)
        if value is None:
            if len(err) > 0:
                flash(err[0], "danger")
            break
        kwargs[key] = value
    else:
        user = crear_usuario(email=google_user_info['email'], username=kwargs['username'], password=kwargs['password'], first_name=google_user_info['given_name'], last_name=google_user_info['family_name'])
        if user is None:
            flash("Error: No se pudo crear el usuario.", "danger")
            return render_template("complete_registration.html.jinja", user_info=google_user_info)
        session['user_id'] = user.id
        return redirect(url_for("home"))

    return render_template("complete_registration.html.jinja", user_info=google_user_info)
