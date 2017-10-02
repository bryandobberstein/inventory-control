from flask_login import UserMixin
from inventory_control import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30))
    author = db.Column(db.String(30))
    description = db.Column(db.Text)
    isbn = db.Column(db.String(15))
    price = db.Column(db.Float)
    in_stock = db.Column(db.Integer)
    location = db.Column(db.Text)

    def __init__(self, title, author, description, isbn, price, in_stock, location):
        self.title = title
        self.author = author
        self.description = description
        self.isbn = isbn
        self.price = price
        self.in_stock = in_stock
        self.location = location

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), index = True, unique = True)
    pwhash = db.Column(db.String(90))

    def set_pwhash(self, password):
        self.pwhash = generate_password_hash(password, method="sha256", salt_length = 12)
    def verify_pwhash(self, password):
        return check_password_hash(self.pwhash, password)

    @staticmethod
    def register(username, password):
        user = User(username = username)
        user.set_pwhash(password)
        db.session.add(user)
        db.session.commit()
        return user
