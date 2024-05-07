from src.core.database import db
from . import base_model

class Comment(base_model.ModelBase):
    __tablename__ = 'comments'
    content = db.Column(db.String(255), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, content, request_id, user_id):
        self.content = content
        self.request_id = request_id
        self.user_id = user_id

    def register_comment_database(self):
        db.session.add(self)
        db.session.commit()