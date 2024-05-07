from src.core.database import db
from src.core.models.user_model import User
from src.core.models.institution_model import Institution
from src.core.models.service_model import Service
from src.core.models.request_model import Request
from src.core.models.request_status_model import RequestStatus
from src.core.models.request_status_change_model import RequestStatusChange
from src.core.models.comment_model import Comment
from src.core.models.type_model import Type
from src.core.models.config_model import Config
from .permission_model import *
from .role_model import *
from .user_model import *
from src.core.bcrypt import bcrypt


def crear_usuario(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def create_institution(**kwargs):
    institution = Institution(**kwargs)
    db.session.add(institution)
    db.session.commit()
    return institution

def create_request(**kwargs):
    request = Request(**kwargs)
    db.session.add(request)
    db.session.commit()
    return request

def create_comment(**kwargs):
    comment = Comment(**kwargs)
    db.session.add(comment)
    db.session.commit()
    return comment

def create_service(**kwargs):
    service = Service(**kwargs)
    db.session.add(service)
    db.session.commit()
    return service

def create_type(**kwargs):
    type = Type(**kwargs)
    db.session.add(type)
    db.session.commit()
    return type


def create_config(**kwargs):
    config = Config(**kwargs)
    db.session.add(config)
    db.session.commit()
    return config    

def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role

def create_permission(**kwargs):
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()
    return permission

def create_request_status(**kwargs):
    request_status = RequestStatus(**kwargs)
    db.session.add(request_status)
    db.session.commit()
    return request_status

def create_request_status_change(**kwargs):
    request_status_change = RequestStatusChange(**kwargs)
    db.session.add(request_status_change)
    db.session.commit()
    return request_status_change