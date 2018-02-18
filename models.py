from flask_login import UserMixin
from inventory_control import db, lm
from flask_bcrypt import generate_password_hash

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
    admin = db.Column(db.Integer)
    new_user = db.Column(db.Integer)

    def __init__(self, username, password, admin = 0, new_user = 1):
        pwhash = generate_password_hash(password).decode('utf-8')
        self.username = username
        self.pwhash = pwhash
        self.admin = admin
        self.new_user = new_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
