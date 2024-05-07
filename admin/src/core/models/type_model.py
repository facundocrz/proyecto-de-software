from src.core.database import db
from . import base_model


class Type(base_model.ModelBase):
    __tablename__ = "types"
    name = db.Column(db.String(64))
    services = db.relationship("Service", back_populates="type")

    def __init__(self, name):
        self.name = name
    
    def get_type(name):
        return Type.query.filter_by(name=name).first()
    
    # listar todos los tipos de servicios

    @staticmethod
    def get_all_types():
        return Type.query.distinct(Type.name).all()
