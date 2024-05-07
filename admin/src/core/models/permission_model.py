from src.core.database import db
from . import base_model
from .role_model import role_has_permission


class Permission(base_model.ModelBase):
    __tablename__ = "permissions"

    name = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    roles = db.relationship("Role", secondary=role_has_permission, back_populates="permissions")

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()