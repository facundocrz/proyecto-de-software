from flask import Blueprint,redirect, render_template, request, url_for, session, flash 
from src.core.models.config_model import Config
from src.core.models import create_config
from src.web.helpers.auth import login_required, has_permission
from src.web.helpers.validations import verify_space, verify_vacio, validate_email_config

config_blueprint = Blueprint("config", __name__, url_prefix="/config")

@config_blueprint.get("/") 
@login_required
@has_permission("config_show")
def index():
    config = Config.get_singleton()

    return render_template("config.html.jinja", config=config)

@config_blueprint.post("/config")
@login_required
@has_permission("config_update")
def update():
   config = Config.get_singleton()

   if verify_vacio(items = request.form.items()):
      if verify_space(items = request.form.items()) :  
         if request.form['cant']:  
            cant = request.form['cant']
         if request.form['contact']:  
            contact = request.form['contact']
         if request.form['email']:     
            email = request.form['email']
         if request.form['state']:  
            state = request.form['state'].lower() == "true"
         if request.form['information']:     
            information = request.form['information']
         if validate_email_config(email)and int(cant) > 0:
            flash("Se actualizo el valor del campo editado", "success")
            config.update_config_database(cant,contact,email,state,information)
      else:
         flash("No se puedo guardar, Actualize bien los campos", "danger")   
   else:
      flash("No se puedo guardar campos vacios", "danger")




   return redirect(url_for("config.index"))
