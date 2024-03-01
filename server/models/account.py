from server import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    joined = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Posts', backref="user", passive_deletes=True)