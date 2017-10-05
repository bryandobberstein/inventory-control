from flask import request, redirect, render_template, session
from werkzeug import generate_password_hash, check_password_hash
from inventory_control import app
from forms import *
from models import *

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
        elif check_password_hash(self.pwhash, password):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get("next") or url_for("search"))
    return render_template("login.html", form = form)

@app.route("/register", methods = ["GET", "POST"])
def register_page():
    form = RegisterForm()
    search_form = SearchForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        pwhash = generate_password_hash(password, method="sha256", salt_length = 12)
        user  = User(username, pwhash)
        db.session.add(user)
        db.session.commit()
        return render_template("search.html", form = SearchForm(), title = "Search", greeting = "Search")
    return render_template("register.html", form = form, title = "Register User", greeting = "Register User")

#TODO (templates)
@app.route("/search", methods = ["GET", "POST"])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        if form.category.data:
            category = form.category.data
            term = form.term.data
            items = Item.query.filter(Item.category.contains(term)).all()
        else:
            term = form.term.data
            items = Item.query.filter(Item.description.contains(term)).all()
        return render_template("results.html", items = items)
    return render_template("search.html", form = form)

#TODO (templates)
@app.route("/new_item", methods = ["GET", "POST"])
def new_item():
    form = AddItemForm()

    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        description = form.description.data
        isbn = form.isbn.data
        price = form.price.data
        in_stock = form.in_stock.data
        location = form.location.data

        double_check = Item.query.filter_by(isbn = isbn)
        if double_check:
            return render_template("add.html", error = "That item already exists")
        else:
            item_to_add = Item(title,author, description, isbn, price, in_stock, location)
            db.session.add(item_to_add)
            db.session.commit()
            newid = item_to_add.id
            new_item_id = Item.query.filter_by(id = id).first()
            return render_template("new_item.html", new_item_id = new_item_id)

    return render_template("add.html")
