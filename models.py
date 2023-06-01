
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(11))
    password_hash = db.Column(db.String(200))
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return "<Store User: {}>".format(self.username)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(50))
    category = db.Column(db.String(50))
    description = db.Column(db.TEXT)
    image = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.now())
    

    def __repr__(self) -> str:
        return "<Product: {}".format(self.title)
