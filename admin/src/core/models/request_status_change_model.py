from src.core.database import db
from . import base_model

class RequestStatusChange(base_model.ModelBase):
    __tablename__ = "request_status_changes"
    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"))
    status_changed_to = db.Column(db.String(64), db.ForeignKey("request_statuses.name"))
    status = db.relationship("RequestStatus", foreign_keys=[status_changed_to])
    observation = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", foreign_keys=[user_id])

    def __init__(self, request_id, status_changed_to, observation, user_id):
        self.request_id = request_id
        self.status_changed_to = status_changed_to
        self.observation = observation
        self.user_id = user_id

    def register_request_database(self):
        db.session.add(self)
        db.session.commit()
   