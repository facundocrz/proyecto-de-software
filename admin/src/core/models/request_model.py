from datetime import datetime
from src.core.database import db
from . import base_model
from src.core.models.institution_model import Institution
from src.core.models.service_model import Service


class Request(base_model.ModelBase):
    __tablename__ = "requests"
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    description = db.Column(db.String(255))
    comments = db.relationship("Comment", backref="request", cascade='all, delete-orphan' )

    status_changes = db.relationship("RequestStatusChange", backref="request", cascade='all, delete-orphan')# cambio estado
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    service = db.relationship("Service", backref="requests")
    current_status = db.Column(db.String(64), db.ForeignKey("request_statuses.name")) #estado actual
    status = db.relationship("RequestStatus", foreign_keys=[current_status])

    def __init__(self, user_id, title, description, service_id):
        self.title = title
        self.user_id = user_id
        self.current_status = "Creada"
        self.description = description
        self.service_id = service_id


    def get_all_paginated(page, per_page):
        return Request.query.paginate(page=page, per_page=per_page, error_out=False)

    def get_all_paginated_by_user(user, page, per_page, sort, order, start_date, end_date, filter):
        query = Request.query.filter_by(user_id=user.id)
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Request.created_at >= start_date)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Request.created_at <= end_date)
        if filter != 'All':
            query = query.filter(Request.current_status == filter)
        if sort:
            if order == "desc":
                query = query.order_by(getattr(Request, sort).desc())
            else:
                query = query.order_by(getattr(Request, sort))
        elif order == "desc":
            query = query.order_by(Request.id.desc())
        return query.paginate(page=page, per_page=per_page, error_out=False)

    def register_request_database(self):
        db.session.add(self)
        db.session.commit()

    def get_request_by_id(self, r_id):
        return Request.query.filter(self.id == r_id).first()

    def delete(self):


        db.session.delete(self)
        db.session.commit()
    
    def update_status(self, status):
        self.current_status = status
        db.session.commit()

    @classmethod
    def _query(cls):
        return db.session.query(cls)
    @classmethod
    def count(cls):
        return cls._query().count()

    @classmethod
    def paginate(cls, page, page_size, filter_title=None, filter_inicio=None, filter_fin=None, filter=None, institution=None):
        q = cls.query.join(Service).join(Institution).filter(Institution.id == institution.id)

        if filter_title:
            q = q.filter(cls.title == filter_title)

 
        if filter_inicio and filter_fin:
            filter_inicio = datetime.strptime(filter_inicio, '%Y-%m-%d')
            filter_fin = datetime.strptime(filter_fin, '%Y-%m-%d')

            q = q.filter(cls.created_at.between(filter_inicio, filter_fin))


        if filter == 'Aceptada':
            q = q.filter(cls.current_status == filter)
        elif filter == 'Cancelada':
            q = q.filter(cls.current_status == filter)
        elif filter == 'Rechazada':
            q = q.filter(cls.current_status == filter)
        elif filter == 'En proceso':
            q = q.filter(cls.current_status == filter)
        elif filter == 'Finalizada':
            q = q.filter(cls.current_status == filter)
    
        return q.paginate(page=page, per_page=page_size, error_out=False), q.count()
    
    def get_status_changes(self):
        return self.status_changes


