from flask import Blueprint,redirect, render_template, request, url_for, session, flash 
from src.core.models.user_model import User
from src.core.models.config_model import Config
from src.web.helpers.auth import login_required


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")   
def login():
    return render_template("auth/login.html.jinja")


@auth_blueprint.post("/authenticate")   
def authenticate():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.check_user(username, password)   
        config = Config.get_singleton()
        if not config.state and user.username != "super":
            flash(config.information, "danger")  
            return redirect(url_for("home"))          
        else:
            if user:
                if user.activo:
                    session['user_id'] = user.id
                    return redirect(url_for("home"))
                elif user.activo == False:
                    flash("El usuario se encuentra desactivado", "danger")      
            else:
                flash("El nombre de usuario o contraseña es incorrecto", "danger")

    return render_template("auth/login.html.jinja")               

# Al acceder a la ruta "/LOGOUT", la sesión se destruirá y el usuario será redirigido 
# a la página principal sin la variable de sesión "usuario". 
@auth_blueprint.get("/logout")
def logout():
    session.pop('google_token', None)
    session.clear()
    return redirect(url_for("home"))