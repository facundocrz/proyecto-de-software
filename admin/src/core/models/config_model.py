from src.core.database import db
from . import base_model
   

class Config(base_model.ModelBase):
    __tablename__ = 'config'

    cant = db.Column(db.Integer)
    contact = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Boolean(), nullable=False)
    information = db.Column(db.String(255), nullable=False)

    def __init__(self, cant, contact,email, state, information):
        self.cant = cant
        self.contact = contact
        self.email = email 
        self.state = state
        self.information = information

    @classmethod
    def get_singleton(cls):
        return cls.find_by_id(1)
    
    def update_config_database(self, cant, contact,email, state, information ):
        self.cant = cant
        self.contact = contact
        self.email = email
        self.state = state
        self.information = information
        db.session.commit()