from src.core.database import db
from . import base_model

class RequestStatus(db.Model):
    __tablename__ = "request_statuses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.name = name