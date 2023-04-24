from flask_login import UserMixin
from app import db


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    pwd = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)

    # def check_password(self):

  
    # def __repr__(self):
    #     return self.username

