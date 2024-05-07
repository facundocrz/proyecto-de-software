import math
from flask import session
from flask import Blueprint,redirect, render_template, request, url_for, flash
from src.core.models.service_model import Service
from src.core.models.institution_model import Institution
from src.core.models.type_model import Type
from src.core.models.config_model import Config
from src.web.helpers.auth import login_required, has_permission
from src.core.models import create_service
from src.web.helpers.session import get_current_institution
from src.core.models import create_service
from src.web.helpers.validations import verify_space, verify_vacio, verify_service,verify_lenghts
service_blueprint = Blueprint("service", __name__, url_prefix="/service")

@service_blueprint.get("/")
@service_blueprint.get("/<int:page>") 
@login_required
@has_permission("service_index")     
def index(page=1):
    config = Config.get_singleton()
    page_size = config.cant
    s, s_count = Service.paginate(
        page, page_size, inst=get_current_institution())
    '''divide la cantidad de todos los servicios en las filas con la cantidad de servicios que quiero por pagina'''
    page_count = math.ceil(s_count / page_size)
    return render_template(
        "service/index.html.jinja",
        s=s,
        s_count=s_count,
        page=page,
        page_count=page_count
    )


@login_required
@service_blueprint.route("/create_service",methods=['GET', 'POST'])  
@has_permission("service_create")  
def create():
    if request.method == 'POST':

        if verify_vacio(items=request.form.items()):

            if verify_space(items=request.form.items()):
                
                if not (verify_service(request.form['title'])) and verify_lenghts(request.form['title'], request.form['description']):
                    s = request.form['state']
                    '''type_id se guarda el valor de opciones que se selecciona en el formulario, estas opciones son los 
                       tipos de servicios que existen
                    s.lower() convierte la cadena "True" o "False" recibida en boolean
                    institution= session.get("inst_id") si ya existe un Servicio con "nombre1" deberia dejar crearlo 
                    por que seria para otra institucion, por simplicidad no dejo que se repitan aun cuando si se 
                    llamaran igual no serian el mismo'''
                    create_service (
                        title=request.form['title'],
                        description=request.form['description'],
                        state = (s.lower()=='true'),
                        keywords=request.form['keywords'], 
                        type_id=request.form['opciones'], 
                        institution= session.get("inst_id")
                    )
            else:
                flash("El servicio no pudo crearse ", "danger")
        else:
            flash("el campo no puede ser vacio", "danger")
            return render_template('service/create_service.html.jinja')

        return redirect(url_for("service.index"))

    return render_template('service/create_service.html.jinja')

@login_required
@service_blueprint.route("/update/<id>",methods=['GET', 'POST']) 
@has_permission("service_update") 
def update(id):
    serv = Service.find_by_id(id)
    '''Idem create() solamente que aca no se accede al estado de habilitacion ni a la institucion'''
    if verify_vacio(items=request.form.items()):
        if verify_space(items=request.form.items()):
            if verify_lenghts(request.form['title'], request.form['description']):
                    title= request.form['title'],
                    description= request.form['description'],
                    keywords=request.form['keywords']
                    type= request.form['opciones']
                    serv.update_service_database(title,description,keywords,type)
                    flash("El servicio se actualizo correctamente ", "succes")
        else:
            flash("El servicio no pudo actualizarse ", "danger")
    else:
        flash("el campo no puede ser vacio", "danger")
    return redirect(url_for("service.index"))



@login_required
@service_blueprint.route("/delete/<id>",methods=['GET', 'POST'])  
@has_permission("service_destroy") 
def delete(id):
    '''Elimina un servicio y redirige al index de servicios'''
    s = Service.get_service_by_id(Service,id)
    s.delete()
    return redirect(url_for("service.index"))


@service_blueprint.route("/enable_disable/<id>",methods=['GET', 'POST'])
@login_required
@has_permission("service_update") 
def enable_disable(id): 
    '''Cambia el estado del servicio. Si estaba habilitado lo deshabilita y viceversa'''
    s = Service.get_service_by_id(Service,id)
    if s.habilite == True :
        s.habilite = False 
    else:
        s.habilite = True
    s.register_service_database()
    return redirect(url_for("service.index"))

