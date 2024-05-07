from flask_jwt_extended import JWTManager


def init(app):
    jwt = JWTManager(app)