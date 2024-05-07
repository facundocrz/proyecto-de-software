from src.core.database import db
from . import base_model
from sqlalchemy.dialects.postgresql import ARRAY
from src.core.models.user_model import user_roles

class Institution(base_model.ModelBase):
    __tablename__ = 'institutions'
    name = db.Column(db.String(100), nullable=False)
    information = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    web = db.Column(db.String(100), nullable=False)
    __db_keywords = db.Column("keywords", db.String(255), default="")
    date_time = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    roles = db.relationship("Role", secondary=user_roles, back_populates="institutions", viewonly=True)
    services = db.relationship("Service", back_populates="institution")

    def __init__(self, name, information, address, location, web, date_time, contact, keywords_list=None, keywords=None):
        self.name = name
        self.information = information
        self.address = address
        self.location = location
        self.web = web
        self.date_time = date_time
        self.contact = contact
        self.activo = True
        if keywords_list is not None:
            self.keywords_list = keywords_list
        if keywords is not None:
            self.keywords = keywords

    @property
    def keywords_list(self):
        return self.__db_keywords.split(",")
    
    @keywords_list.setter
    def keywords_list(self, value):
        self.__db_keywords = ",".join(value)
    
    @property
    def keywords(self):
        return ", ".join(self.keywords_list)
    
    @keywords.setter
    def keywords(self, value):
        self.keywords_list = [k.strip() for k in value.split(",")]

    def get_all_paginated(page, per_page):
        return Institution.query.paginate(page=page, per_page=per_page, error_out=False)
    
    def get_all_active_paginated(page, per_page):
        return Institution.query.filter_by(activo=True).paginate(page=page, per_page=per_page, error_out=False)

    def add_service(self, service):
        self.services.append(service)
        db.session.commit()

    def register_inst_database(self):
        db.session.add(self)
        db.session.commit()
        
    def list_institutions():
        return Institution.query.all()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_inst_database(self, name, information, address, location, web ,keywords,date_time,contact ):
        self.name = name
        self.information = information
        self.address = address
        self.location = location
        self.web = web
        self.keywords = keywords
        self.date_time = date_time
        self.contact = contact
        db.session.commit()
    
    def get_user_roles(self, page, page_size):
        q = db.session.query(user_roles).filter_by(institution_id=self.id)
        return q.paginate(page=page, per_page=page_size), q.count()

    @classmethod
    def _query(cls):
        return db.session.query(cls)
    
    @classmethod
    def paginate(cls, page, page_size):
        return cls._query().paginate(page=page, per_page=page_size, error_out=False)
    
    @classmethod
    def count(cls):
        return cls._query().count()
