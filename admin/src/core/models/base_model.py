from datetime import datetime
from src.core.database import db


class ModelBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def get_fecha(self):
        return self.created_at
