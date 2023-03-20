from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.String, primary_key=True, unique=True, default=get_uuid)
    email  = db.Column(db.String, unique=True)
    password = db.Column(db.Text, nullable=False)
