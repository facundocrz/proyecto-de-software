from src.core.database import db
from . import base_model
from sqlalchemy.dialects.postgresql import ARRAY
from src.core.models.type_model import Type
from src.core.models.institution_model import Institution
from sqlalchemy import or_


class Service(base_model.ModelBase):
    __tablename__ = "services"
    title = db.Column(db.String(64))
    description = db.Column(db.String(255))
    __db_keywords = db.Column("keywords", db.String(255), default="")
    '''  type_id es la relacion 1 a muchos '''
    type_id = db.Column(db.Integer, db.ForeignKey('types.id')) 
    type = db.relationship("Type", back_populates="services") 
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    '''Es el servicio que brinda la institucion'''
    institution = db.relationship("Institution", back_populates="services")
    habilite = db.Column(db.Boolean(), default=True)


    def __init__(self, title, description, type_id, institution=None,state=True, keywords_list=None, keywords=None):
        self.title = title
        self.description = description
        self.type_id = type_id
        self.institution_id = institution
        self.habilite = state
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
        self.keywords_list = [k.strip() for k in value.split(",") if k.strip()]

    def get_all_active_paginated_by_search(q, type_name, page, per_page):
        '''realiza una consulta al bd utilizando la biblioteca SQLAlchemy. Recupera registros de la tabla Service  ''' 
        services = Service.query.filter_by(habilite=True).join(Institution).filter(Institution.activo==True)
        title_filter = Service.title.like(f"%{q}%") 
        desc= Service.description.like(f"%{q}%") 
        ints = Service.institution.has(Institution.name.like(f"%{q}%"))
        keyword_filter = Service.__db_keywords.like(f"%{q}%")
        '''Si me llega una busqueda tambien por tipo de servicio entra por el if'''
        if type_name:
            type_filter = Type.name == type_name
            services = services.join(Type).filter(
                (title_filter | desc | ints |keyword_filter) & type_filter)
        else:
            services = services.filter(
                title_filter | desc | ints | keyword_filter)
        services = services.distinct()
        return services.paginate(page=page, per_page=per_page, error_out=False)

    def get_service(id):
        return Service.query.filter_by(id=id).first()
    
    def get_active_service_in_active_institution(id):
        return Service.query.filter_by(id=id, habilite=True).join(Institution).filter_by(activo=True).first()

    def get_all_types():
        '''with_entities devuelve todos los tipos(Analisis,Consultoria y Desarrollo)
          que hay en la table y el distinct para que no se repitan'''
        return Service.query.with_entities(Service.type).distinct().all()


    def register_service_database(self):
        db.session.add(self)
        db.session.commit()

    def list_services():
        return Service.query.all()

    def get_service_by_id(self, service_id):
        return Service.query.filter(self.id == service_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_service_database(self, title, description, keywords, type_id):
        self.title = title
        self.description = description
        self.keywords = keywords
        self.type_id = type_id
        db.session.commit()
    
    @classmethod
    def _query(cls):
        return db.session.query(cls)

    @classmethod
    def count(cls):
        return cls._query().count()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def paginate(cls, page, page_size, inst=None):
        q = cls._query()
        if inst:
            q = q.filter_by(institution_id=inst.id)

        return q.paginate(page=page, per_page=page_size, error_out=False), q.count()
