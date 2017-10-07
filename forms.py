from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, IntegerField, FloatField, BooleanField, SubmitField, HiddenField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo
from models import *

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired(), Length(6, 20)])
    password = PasswordField("Password", validators = [InputRequired(), Length(6, 20)])
    verify = PasswordField("Verify Password", validators = [InputRequired(), EqualTo("password")])
    admin = BooleanField("Give User Admin Rights")
    submit = SubmitField("Register")

class DeleteUserForm(FlaskForm):
    uid = HiddenField()
    delete = SubmitField("Delete")

class AddItemForm(FlaskForm):
    title = StringField("Title", validators = [InputRequired()])
    author = StringField("Author", validators = [InputRequired()])
    description = TextField("Description", validators = [InputRequired()])
    isbn = isbn = IntegerField("ISBN", validators = [InputRequired()])
    price = FloatField("Price", validators = [InputRequired()])
    in_stock = IntegerField("# in stock", validators = [InputRequired()])
    location = TextField("Location", validators = [InputRequired()])
    submit = SubmitField("Add Item")

class SearchForm(FlaskForm):
    term = StringField("Search")
    category = SelectField("Search In", choices = [("all", "All"), ("title", "Title"), ("author", "Author"), ("isbn", "ISBN")])
    submit = SubmitField("Find")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators = [InputRequired(), Length(6, 20)])
    verify = PasswordField("Verify Password", validators = [InputRequired(), EqualTo("password")])
    submit = SubmitField("Change Password")

class UpdateItemForm(FlaskForm):
    uid = HiddenField()
    title = StringField("Title", validators = [InputRequired()])
    author = StringField("Author", validators = [InputRequired()])
    description = TextField("Description", validators = [InputRequired()])
    isbn = isbn = IntegerField("ISBN", validators = [InputRequired()])
    price = FloatField("Price", validators = [InputRequired()])
    in_stock = IntegerField("# in stock", validators = [InputRequired()])
    location = TextField("Location", validators = [InputRequired()])
    delete = BooleanField("Delete Item From Inventory")
    submit = SubmitField("Update Item")
