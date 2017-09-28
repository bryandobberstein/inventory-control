from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, TextField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/max/Documents/git/inventory-control/database/inventory.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "JinUdceer0"

lm = LoginManager(app)
lm.login_view = "login"
bootstrap = Bootstrap(app)
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
    isbn = db.Column(db.String(15))
    price = db.Column(db.Float)
    location = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def __init__(self, name, description, isbn, price, location, category):
        self.name = name
        self.description = description
        self.price = price
        self.location = location
        self.isbn = isbn
        self.category = category

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

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class TestForm(FlaskForm):
    name = StringField("Name", validators = [InputRequired(message = "Please enter a name")])
    submit = SubmitField("Enter")

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired(), Length(6, 20)])
    password = PasswordField("Password", validators = [InputRequired(), Length(8, 20)])
    verify = PasswordField("Verify Password", validators = [InputRequired(), EqualTo(password)])
    submit = SubmitField("Register")

@app.route("/", methods = ["GET", "POST"])
def index():
    form = TestForm()
    name = ""
    error = ""
    greeting = "Enter Your Name"
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            greeting = "Hello, {}".format(name)
    return render_template("index.html", form = form, greeting = greeting, title = "Inventory Control")

@app.route("/login", methods = ["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.verify_pwhash(form.password.data):
            return redirect(url_for("login"))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get("next") or url_for("search"))
    return render_template("login.html", form = form)

@app.route("/register", methods = ["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        User.register(username, password)
        return render_template("inventory-search.html")

#TODO
@app.route("/search", methods = ["GET", "POST"])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        if category:
            category = form.category.data
            term = form.term.data
            items = Item.query.join(Category.query.filter_by(category).filter(Item.description.contains(term))).all()
        else:
            items = Item.query.query.filter(Item.description.contains(term)).all()


if __name__ == "__main__":
    app.run()
