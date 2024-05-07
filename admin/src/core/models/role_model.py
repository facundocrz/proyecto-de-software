from src.core.database import db
from . import base_model
from src.core.models.user_model import user_roles


role_has_permission = db.Table(
    "role_has_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True)
)


class Role(base_model.ModelBase):
    __tablename__ = "roles"

    name = db.Column(db.String(64))
    users = db.relationship("User", secondary=user_roles, back_populates="roles", viewonly=True)
    institutions = db.relationship("Institution", secondary=user_roles, back_populates="roles", viewonly=True)
    permissions = db.relationship("Permission", secondary=role_has_permission, back_populates="roles", viewonly=True)

    def __init__(self, name):
        self.name = name
    
    def add_permission(self, permission):
        ins = role_has_permission.insert().values(role_id=self.id, permission_id=permission.id)
        db.session.execute(ins)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
