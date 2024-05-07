import math
from flask import abort, Blueprint, redirect, render_template, request, url_for, session, flash
from src.core.models import create_institution
from src.core.models.institution_model import Institution
from src.core.models.role_model import Role
from src.core.models.user_model import User
from src.core.models.config_model import Config
from src.web.helpers.auth import login_required, has_permission, check_permission
from src.web.helpers.session import get_current_user, get_current_institution
from src.web.helpers.validations import verify_space, verify_vacio
from src.core.models.service_model import Service


institutions_blueprint = Blueprint("institutions", __name__, url_prefix="/institutions")


@institutions_blueprint.get("/")
@institutions_blueprint.get("/<int:page>") 
@login_required
@has_permission("institution_index")
def index(page=1):
    config = Config.get_singleton()
    page_size = config.cant
    inst_count = Institution.count()
    page_count = math.ceil(inst_count / page_size)

    services = Service.query.all()   

    return render_template(
        "institutions/index.html.jinja",
        inst=Institution.paginate(page, page_size),
        inst_count=inst_count,
        page=page,
        page_count=page_count,
        services = services
    )


@institutions_blueprint.route("/create_inst", methods=['GET', 'POST'])
@login_required
@has_permission("institution_create")
def create():
    if request.method == 'POST':

        if verify_vacio(items = request.form.items()):
            if verify_space(items = request.form.items()):               
                create_institution(
                    name=request.form['name'],
                    information=request.form['information'],
                    address=request.form['address'],
                    location=request.form['location'],
                    web=request.form['web'],
                    keywords=request.form['keywords'],
                    date_time=request.form['date_time'],
                    contact =request.form['contact']
                )
            else: 
                flash("la institucion No pudo crearse ", "danger")   
        else:
            flash("el campo no puede ser vacio", "danger")
            return render_template('institutions/create.html.jinja')

        return redirect(url_for("institutions.index"))
    
    return render_template('institutions/create.html.jinja')



@institutions_blueprint.post("/update/<id>")
@login_required
@has_permission("institution_update")
def update(id):
    inst = Institution.find_by_id(id)

    if verify_vacio(items = request.form.items()):
        if verify_space(items = request.form.items()): 

            name= request.form['name']
            information= request.form['information']
            address = request.form['address']
            location = request.form['location']
            web = request.form['web']
            keywords= request.form['keywords']
            date_time= request.form['date_time']
            contact = request.form['contact']

            inst.update_inst_database( name, information, address, location, web ,keywords,date_time,contact)
            flash("la institucion Se Actualizo correctamente ", "succes")  
        else: 
            flash("la institucion No pudo Actualizarse ", "danger")   
    else:
        flash("el campo no puede ser vacio", "danger")

    

    return redirect(url_for("institutions.index"))  



@institutions_blueprint.route("/delete/<id>",methods=['GET', 'POST'])
@login_required   
@has_permission("institution_destroy")
def delete(id):
    inst = Institution.find_by_id(id)
    inst.delete()

    return redirect(url_for("institutions.index"))


@institutions_blueprint.route("/activate_deactivate/<id>",methods=['GET', 'POST'])
@login_required
@has_permission("institution_activate", "institution_deactivate")
def activate_deactivate(id):
    inst = Institution.find_by_id(id)
    inst.activo = not inst.activo
    
    inst.register_inst_database()
    return redirect(url_for("institutions.index"))