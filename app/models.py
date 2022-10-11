#from cop4521 import db
from . import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String(140))
    by = db.Column(db.String(140))
    title = db.Column(db.String(140))
    url = db.Column(db.String(500))

    def __repr__(self):
        return '<Post {} by {} : {}>'.format(self.title, self.by, self.id)
