from flask import session
from src.core.models.institution_model import Institution
from src.core.models.role_model import Role
from src.core.models.user_model import User


def get_current_user():
    return User.find_by_id(session.get("user_id"))


def get_current_institution():
    return Institution.find_by_id(session.get("inst_id"))


def is_superadmin():
    user = get_current_user()
    return user.has_role(Role.get_by_name("Super Administrador")) if user else None