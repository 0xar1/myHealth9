from . import db,login
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    full_name = db.Column(db.String(200))


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    def get_id(self):
           return (self.uid)

@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class experience(db.Model):
    exp_id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    buyerName = db.Column(db.String(50))
    likes = db.Column(db.Integer,default = 0)
    dislikes = db.Column(db.Integer,default = 0)