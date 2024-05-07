from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init(app):
    db.init_app(app)
    config(app)


def config(app):
    @app.teardown_request
    def close_session(exception=None):
        db.session.close()



def reset_db():
    print("Eliminando base de datos...")
    db.drop_all()
    print("Creando base de datos...")
    db.create_all()
    print("Done!")
