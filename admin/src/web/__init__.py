from flask import Flask, render_template
from flask_session import Session
from flask_cors import CORS
from flask_mail import Mail
from src.web import error
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.controllers.auth_controller import auth_blueprint
from src.web.controllers.google_auth_controller import google_auth_blueprint
from src.web.controllers.user_controller import user_blueprint
from src.web.controllers.institutions_controller import institutions_blueprint
from src.web.controllers.config_controller import config_blueprint
from src.web.controllers.role_controller import role_blueprint
from src.web.controllers.inst_controller import inst_blueprint
from src.web.controllers.service_controller import service_blueprint
from src.web.controllers.service_request_controller import service_request_blueprint
from src.web.helpers import list_institutions
from src.web.helpers import auth
from src.web.helpers.session import get_current_user, get_current_institution, is_superadmin
from src.web.api.controllers.institution_api_controller import api_institution_bp
from src.web.api.controllers.auth_api_controller import api_auth_bp
from src.web.api.controllers.user_api_controller import api_user_bp
from src.web.api.controllers.service_api_controller import api_service_bp
from src.web.api.controllers.contact_api_controller import api_contact_bp
from src.web.api.controllers.stats_api_controller import api_stats_bp
from src.web.api.controllers.state_api_controller import api_state_bp
from src.core import jwt
from flask_cors import CORS
from src.core.google import google


def create_app(env="development", static_folder="../../static", template_folder="templates"):
    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
    
    app.config.from_object(config[env])
    database.init(app)

    CORS(app)

    from . import mail
    mail.init_app(app)
    
    # Server Side session
    Session(app)
    jwt.init(app)

    @app.get("/")
    def home():
        return render_template("home.html.jinja")   
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(google_auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(institutions_blueprint)
    app.register_blueprint(service_blueprint)
    app.register_blueprint(service_request_blueprint)
    app.register_blueprint(config_blueprint)
    app.register_blueprint(role_blueprint)
    app.register_blueprint(inst_blueprint)

    app.register_blueprint(api_institution_bp)
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(api_user_bp)
    app.register_blueprint(api_service_bp)
    app.register_blueprint(api_contact_bp)
    app.register_blueprint(api_stats_bp)
    app.register_blueprint(api_state_bp)

    app.register_error_handler(404, error.not_found)

    app.jinja_env.globals.update(
        is_authenticated=auth.authenticated,
        list_institutions=list_institutions,
        get_current_user=get_current_user,
        get_current_institution=get_current_institution,
        is_superadmin=is_superadmin,
        check_permission=auth.check_permission
    )

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seeds")
    def seedsdb():
        seeds.run()

    return app