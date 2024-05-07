from flask import session, redirect, request, url_for,flash
from src.core.models.institution_model import Institution
from src.core.models.role_model import Role
from src.core.models.permission_model import Permission
from src.core.models.user_model import User
from src.web.helpers.session import get_current_user, get_current_institution
from functools import wraps

# Utilidades y decoradores de autenticación.

def authenticated():
    return session.get("user_id") is not None


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not authenticated():            
            flash("Es necesario iniciar sesión para relaizar esta operación.", "danger")    
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    
    return wrap


def check_permission(*permissions, institution=None):
    if not authenticated():
        return False

    permissions = set(permissions)
    
    user = get_current_user()

    if not institution:
        institution = get_current_institution()

    roles = user.get_roles(inst=institution)

    for r in roles:
        r = Role.get_by_id(r.role_id)
        if permissions.issubset(set([p.name for p in r.permissions])):
            return True
    
    return False


def has_permission(*permissions):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            nonlocal permissions

            if not authenticated():
                return redirect(url_for('home'))  

            inst_id = session.get("inst_id")
            inst = Institution.find_by_id(inst_id) if inst_id else None

            if check_permission(*permissions, institution=inst):
                return f(*args, **kwargs)
            else:
                flash("No tiene los permisos necesarios para realizar esta operación.", "danger")
                return redirect(url_for('home'))            
        
        return wrap
    
    return decorator