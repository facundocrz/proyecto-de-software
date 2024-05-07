import bcrypt
from sqlalchemy import or_
from src.core.bcrypt import bcrypt
from src.core.database import db
from . import base_model


user_roles = db.Table(
    "user_roles",
    db.Column("id", db.Integer, primary_key=True, unique=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("institution_id", db.Integer, db.ForeignKey("institutions.id"), nullable=True),
)


class User(base_model.ModelBase):
    __tablename__ = "users"

    email = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    activo = db.Column(db.Boolean, default=True)

    # username y password son null cuando el usuario todavia no confirmo por email
    username = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    roles = db.relationship("Role", secondary=user_roles, back_populates="users", viewonly=True)
    requests = db.relationship("Request", backref="user")

    def __init__(self, email, first_name, last_name, activo=True, username=None, password=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.activo = activo
        self.username = username
        if password is not None:
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    @property
    def exists(self):
        return self.username is not None and self.password is not None

    def update(self, **kwargs):
        password = kwargs.get('password')
        if password:
            password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
            password = password_hash.decode('utf-8')
            kwargs['password'] = password

        for k, v in kwargs.items():
            setattr(self, k, v)
        
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def has_role(self, role, inst=None):
        q = db.session.query(user_roles).filter_by(user_id=self.id, role_id=role.id)
        if inst:
            q = q.filter_by(institution_id=inst.id)
        
        return q.count() > 0

    def add_role(self, role, inst=None):
        if inst:
            ins = user_roles.insert().values(user_id=self.id, role_id=role.id, institution_id=inst.id)
        else:
            ins = user_roles.insert().values(user_id=self.id, role_id=role.id)
        
        db.session.execute(ins)
        db.session.commit()
    
    def remove_role(self, role, inst=None):
        q = db.session.query(user_roles).filter_by(user_id=self.id, role_id=role.id)
        if inst:
            q = q.filter_by(institution_id=inst.id)

        n = q.count()
        q.delete()
        db.session.commit()

        return n > 0
    
    def get_roles(self, inst=None):
        q = db.session.query(user_roles).filter_by(user_id=self.id)
        if inst:
            q = q.filter(or_(user_roles.c.institution_id == None, user_roles.c.institution_id == inst.id))
        
        return q
    
    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.username != None).all()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter(cls.username != None).filter_by(email=email).first()

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter(cls.username != None).filter_by(username=username).first()

    @classmethod
    def find_user(cls, username):
        user = cls.find_user_by_email(username)
        if not user:
            user = cls.find_user_by_username(username)
        return user
    
    @classmethod
    def check_user(cls, username, password):
        user = cls.find_user(username)
        if user and bcrypt.check_password_hash(user.password, password.encode('utf-8')):
            return user
        
        return None

    @classmethod
    def _query(cls):
        return db.session.query(cls)
    
    @classmethod
    def _filter(cls, f):
        return cls._query().filter(f)
    
    @classmethod
    def _filter_id(cls, id):
        return cls._filter(cls.id == id)
    
    @classmethod
    def get(cls, id):
        return cls._filter_id(id).first()
    
    @classmethod
    def count(cls):
        return cls._query().count()

    @classmethod
    def paginate(cls, page, page_size, filter_email=None, filter_active=None):
        q = cls._query().filter(cls.username != None)

        if filter_email:
            q = q.filter(cls.email == filter_email)

        if filter_active == 'active':
            q = q.filter(cls.activo == True)
        elif filter_active == 'blocked':
            q = q.filter(cls.activo == False)

        return q.paginate(page=page, per_page=page_size, error_out=False), q.count()
    
    @classmethod
    def create(cls, **kwargs):
        user = User()
        db.session.add(user)
        user.update(**kwargs)

        return user
    
    def get_fecha(self):
        return self.created_at

    @classmethod
    def get_username_by_id(cls,user_id):
        return cls.query.filter(cls.username != None).filter_by(id=user_id).first().username
