from src.core.models.institution_model import Institution
from src.web.helpers.auth import check_permission


def list_institutions():
    return [inst for inst in Institution.get_all() if inst.activo and check_permission(institution=inst)]