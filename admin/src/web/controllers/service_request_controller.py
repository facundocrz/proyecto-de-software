from datetime import datetime
import math
from flask import Blueprint,redirect, render_template, request, url_for, session, flash 
from src.core.models.request_model import Request
from src.core.models.request_status_change_model import RequestStatusChange
from src.core.models import create_request_status_change
from src.core.models.config_model import Config
from src.core.models.user_model import User
from src.core.models.service_model import Service
from src.core.models.comment_model import Comment
from src.web.helpers.auth import login_required
from src.web.helpers.session import get_current_institution
from src.core.models import create_comment
from src.web.helpers.validations import verify_space, verify_vacio

service_request_blueprint = Blueprint("service_request", __name__, url_prefix="/service_request")

@service_request_blueprint.get("/") 
@service_request_blueprint.get("/<int:page>") 
@login_required    
def index(page=1): 
    users = User.query.all()   
    servi = Service.query.all()   
    comment = Comment.query.all()   
    config = Config.get_singleton()
    requestStatus = RequestStatusChange.query.all()   
    page_size = config.cant

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    filter = request.args.get('filter')

    re, re_count = Request.paginate(page, page_size, request.args.get("title"),fecha_inicio,fecha_fin,filter, get_current_institution())

    page_count = math.ceil(re_count / page_size)


    return render_template(
        "service_request/index.html.jinja", 
        r = re,
        com= comment,
        users= users,
        servi= servi,
        re_count=re_count,
        requestStatus =requestStatus,
        page=page,
        page_count=page_count,
        filter_title=request.args.get("title", ""),
        fecha_inicio = request.args.get("fecha_inicio", ""),
        fecha_fin = request.args.get("fecha_fin", ""),
        filter =  request.args.get("filter", ""),
        get_username = User.get_username_by_id,
    )


@service_request_blueprint.route("/delete/<id>",methods=['GET', 'POST'])
@login_required    
def delete(id):
    re = Request.get_request_by_id(Request,id)
    re.delete()
    return redirect(url_for("service_request.index"))


@service_request_blueprint.route("/chage_status/<id>",methods=['GET', 'POST'])
@login_required
def chage_status(id):
    re = Request.get_request_by_id(Request,id)
    if request.method == "POST":
        if request.form.get('current_status') != "Rechazada" or request.form.get('current_status') != "Cancelada" :

            request_id = id
            status_changed_to = request.form.get('current_status') 
            observation = request.form['observation']
            re2 = create_request_status_change(request_id = request_id,status_changed_to =status_changed_to,observation = observation, user_id=session["user_id"])          
            re.update_status(status_changed_to)
            return redirect(url_for("service_request.index"))
        else:
            flash("No puede cambiar el estado Cancelado, Finalizado","danger")
    
    return redirect(url_for("service_request.index"))

@service_request_blueprint.route("/comment/<id>/<user_id>",methods=['GET', 'POST'])
@login_required
def comment(id,user_id):

    if verify_vacio(items = request.form.items()):
        if verify_space(items = request.form.items()): 

            if request.method == "POST":
                content = request.form['content']
                request_id = id
                user_id = user_id         
                com = create_comment(content=content, request_id=request_id, user_id=user_id)
                flash("Comentario realizado con exito", "success")
                return redirect(url_for("service_request.index"))
        else: 
            flash("la institucion No pudo Actualizarse ", "danger")   
    else:
        flash("el campo no puede ser vacio", "danger")
    
    return redirect(url_for("service_request.index"))





 



