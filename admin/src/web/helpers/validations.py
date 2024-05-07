import re
from src.core.models.user_model import User
from flask import flash
from src.core.models.service_model import Service

def validate_email(form, user):
    email = form.get("email")

    if email is None or len(email) <= 0:
        return None, "Por favor, ingrese una dirección de correo electrónico"
    
    if len(email) > 32:
        return None, "La dirección de correo electrónico ingresada es muy larga"
    
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(regex, email):
        return None, "La dirección de correo electrónico ingresada no es válida"
    
    same = User.find_user_by_email(email)
    if same and same != user:
        return None, "Ya existe un usuario con la misma dirección de correo electrónico ingresada"
    
    return (email,)


def validate_username(form, user):
    username = form.get("username")

    if username:
        username = username.strip()
    else:
        username = ''

    if not username:
        return None, "Por favor, ingrese un nombre de usuario"
    
    if len(username) < 4:
        return None, "El nombre de usuario ingresado es muy corto"
    
    if len(username) > 20:
        return None, "El nombre de usuario ingresado es muy largo"
    
    if any(not (c.isalpha() or c.isdigit() or c == '.' or c == '_') for c in username):
        return None, f"El nombre de usuario solo puede contener letras, números, '.' y '_'"
    
    same = User.find_user_by_username(username)
    if same and same != user:
        return None, "Ya existe un usuario con el mismo nombre de usuario ingresado"

    return (username,)


def validate_password(form, user):
    password = form.get("password")

    if not password:
        return None, "Por favor, ingrese una contraseña"
    
    if len(password) < 4:
        return None, "La contraseña debe tener cuatro o más caracteres"
    
    if len(password) > 32:
        return None, "La contraseña debe tener menos de 32 caracteres"
    
    if any(c.isspace() for c in password):
        return None, f"La contraseña no puede contener caracteres en blanco"
    
    if form.get("password_repeat") != password:
        return None, "Las contraseñas ingresadas no coinciden"

    return (password,)


def validate_name(form, key, msg):
    name = form.get(key)

    if name:
        name = " ".join(name.split())
    else:
        name = ""

    if not name:
        return None, f"Por favor, ingrese un {msg}"
    
    if len(name) < 2:
        return None, f"El/los {msg}/s ingresado es muy corto"
    
    if len(name) > 24:
        return None, f"El/los {msg}/s ingresado es muy largo"
    
    if any(not (c.isalpha() or c.isspace()) for c in name):
        return None, f"El/los {msg}/s solo pueden contener letras y espacios"
    
    return (name,)


def validate_first_name(form, user):
    return validate_name(form, "first_name", "nombre")


def validate_last_name(form, user):
    return validate_name(form, "last_name", "apellido")


def validate_active(form, user):
    active = form.get("active")
    return (bool(active),)


'''verificacion de espacios en blanco'''
def verify_space(items):

    for clave,valor in items:
        if valor.isspace():
            msg_error = f"El campo {clave} no puede contener espacios en blanco "
            flash(msg_error, "danger")
            return False

    return True


'''verificacion de campos vacios'''
def verify_vacio(items):

    for clave,valor in items:
        if valor == '':
            msg_error = f"El campo {clave} esta vacio"
            flash(msg_error, "danger")
            return False

    return True


def validate_email_config(email):

    if email is None or len(email) <= 0:
        flash("Por favor, ingrese una dirección de correo electrónico","danger")
        return False
    
    if len(email) > 32:
        flash("La dirección de correo electrónico ingresada es muy larga","danger")
        return False
    
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(regex, email):
        flash("La dirección de correo electrónico ingresada no es válida","danger")
        return False
    
    return True


'''Verificacion de que no exista un Servicio con el nombre ingresado'''
def verify_service(title, s=None):
    servicio = Service.query.filter_by(title=title).first()
    if servicio is not None and servicio != s:
        flash("El Servicio ingresado ya existe")
        return True
    return False


''' Verificacion de que las keywords no me lleguen vacias '''
def verify_keywords(k):
    for clave, valor in k:
        if valor == '':
            msg_error = f"El campo {clave} esta vacio"
            flash(msg_error, "danger")
            return False

    return True


'''Verificacion de la cantidad de caracteres del titulo y descripcion de un servicio'''
def verify_lenghts(title, description):
    # Title
    if len(title) > 40:
        flash("Titulo muy largo, el mismo debe tener entre 5 y 40 caracteres")
        return False
    elif len(title) < 5:
        flash("Titulo muy corto, el mismo debe tener entre 5 y 40 caracteres")
        return False
    # description
    if len(description) > 50:
        flash("Descripcion muy larga, la misma debe tener entre 10 y 50 caracteres")
        return False
    elif len(description) < 10:
        flash("Descripcion muy corta, la misma debe tener entre 10 y 50 caracteres")
        return False
    return True
