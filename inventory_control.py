from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/max/Documents/git/inventory-control/database/inventory.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "JinUdceer0"

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    item = db.relationship("Item", backref = "category", lazy = "dynamic")

    def __init__(self, name):
        self.name = name

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    serial_number = db.Column(db.String(50))
    sku = db.Column(db.String(50))
    price = db.Column(db.Float)
    location = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __init__(self, name, description, sku, price, location, serial_number = "NA"):
        self.name = name
        self.description = description
        self.sku = sku
        self.price = price
        self.location = location
        self.serial_number = serial_number

class TestForm(FlaskForm):
    name = StringField("Name", validators = [InputRequired(message = "Name required")])
    submit = SubmitField("Enter")

@app.route("/", methods = ["GET", "POST"])
def index():
    form = TestForm()
    name = ""
    greeting = "Enter Your Name"
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            hashed_name = generate_password_hash(name, method="sha512", salt_length = 10)
            check = check_password_hash(hashed_name, name)
            greeting = "Hello, {}. {}. {}".format(name, hashed_name, check)
        else:
            greeting = "NOTHING ENTERED"
    return render_template("index.html", form = form, greeting = greeting)

if __name__ == "__main__":
    app.run()
