from flask import request, redirect, render_template, session
from werkzeug import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from inventory_control import app, lm
from forms import *
from models import *



@app.route("/", methods = ["GET", "POST"])
def index():
    greeting = "Inventory Control System"
    form = SearchForm()
    lform = LoginForm()
    return render_template("index.html", form = form, lform = lform, greeting = greeting, title = "Inventory Control")

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        password = form.password.data
        pwhash = generate_password_hash(password, method="sha256", salt_length = 12)
        if user is None or not check_password_hash(pwhash, password):
            return redirect("login")
        elif check_password_hash(pwhash, password):
            login_user(user, form.remember_me.data)
            if int(user.new_user) == 1:
                return redirect("change_pw")
            return redirect(request.args.get("next") or "search")
    return render_template("login.html", form = form)

@app.route("/change_pw", methods = ["GET", "POST"])
@login_required
def change_pw():
    form = ChangePasswordForm()
    good = False
    username = current_user.username
    if form.validate_on_submit():
        password = form.password.data
        pwhash = generate_password_hash(password, method="sha256", salt_length = 12)
        user = User.query.filter_by(username = username).first()
        user.new_user = 0
        db.session.commit()
        return redirect("search")
    return render_template("change_pw.html", form = form, greeting = "Change Password", new_user = 1)

@app.route("/lougout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return render_template("logout.html", greeting = "You are now logged out")

@app.route("/register", methods = ["GET", "POST"])
@login_required
def register():
    if current_user.new_user == 1:
        return redirect("change_pw")
    elif current_user.admin == 0:
        return redirect("search")
    form = RegisterForm()
    search_form = SearchForm()
    admin = 0
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if form.admin.data:
            admin = 1
        user  = User(username, password, admin)
        db.session.add(user)
        db.session.commit()
        return render_template("search.html", form = SearchForm(), title = "Search", greeting = "Search")
    return render_template("register.html", form = form, title = "Register User", greeting = "Register User")

@app.route("/delete_user", methods = ["GET", "POST"])
@login_required
def delete_user():
    if current_user.new_user == 1:
        return redirect("change_pw")
    elif current_user.admin == 0:
        return redirect("search")

    form = DeleteUserForm()
    users = User.query.all()
    if form.validate_on_submit():
        id = form.uid.data
        duser = User.query.filter_by(id = id).first()
        if duser.username == "Admin":
            error = "Admin cannot be deleted"
            return render_template("delete_user.html", form = form, users = users, error = error)
        else:
            db.session.delete(duser)
            db.session.commit()

            return render_template("delete_user.html", form = form, users = users)

    return render_template("delete_user.html", form = form, users = users)

@app.route("/search", methods = ["GET", "POST"])
@login_required
def search():
    if current_user.new_user == 1:
        return redirect("change_pw")
    form = SearchForm()

    if form.validate_on_submit():
        if form.category.data == 'title':
            term = form.term.data
            items = Item.query.filter(Item.title.contains(term)).all()
        elif form.category.data == 'author':
            term = form.term.data
            items = Item.query.filter(Item.author.contains(term)).all()
        elif form.category.data == 'isbn':
            term = form.term.data
            items = Item.query.filter(Item.isbn.contains(term)).all()
        else:
            term = form.term.data
            items = Item.query.filter(Item.description.contains(term)).all()
        if not items:
            return render_template("results.html", greeting = term + "  not found")
        return render_template("results.html", items = items)
    return render_template("search.html", form = form)

@app.route("/new_item", methods = ["GET", "POST"])
@login_required
def new_item():
    if current_user.new_user == 1:
        return redirect("change_pw")
    form = AddItemForm()

    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        description = form.description.data
        isbn = form.isbn.data
        price = form.price.data
        in_stock = form.in_stock.data
        location = form.location.data


        item_to_add = Item(title,author, description, isbn, price, in_stock, location)
        db.session.add(item_to_add)
        db.session.commit()
        items = Item.query.filter_by(id = item_to_add.id).all()
        greeting = "Item Added"
        return render_template("results.html", items = items, greeting = greeting)

    return render_template("add.html", form = form)

@app.route("/update", methods = ["POST"])
@login_required
def update():
    if current_user.new_user == 1:
        return redirect("change_pw")
    id = request.form["id"]
    item = Item.query.filter_by(id = id).first()
    form = UpdateItemForm()

    return render_template("update.html", form = form, greeting = "Update Item", item = item)

@app.route("/update_item", methods = ["POST"])
@login_required
def update_item():
    if current_user.new_user == 1:
        return redirect("change_pw")
    form = UpdateItemForm()
    greeting = "Updated"
    if form.validate_on_submit():
        id = form.uid.data
        item = Item.query.filter_by(id = id).first()
        if form.delete.data:
            db.session.delete(item)
            db.session.commit()
            return render_template("deleted.html", greeting = form.title.data + " Deleted")
        else:
            item.title = form.title.data
            item.author = form.author.data
            item.description = form.description.data
            item.isbn = form.isbn.data
            item.price = form.price.data
            item.in_stock = form.in_stock.data
            item.location = form.location.data
            db.session.commit()
            items = Item.query.filter_by(id = id).all()
            return render_template("results.html", items = items, greeting = greeting)

    return render_template("error.html", greeting = "Page Accessed In Error")
