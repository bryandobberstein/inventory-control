from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, IntegerField, FloatField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

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
    password = PasswordField("Password", validators = [InputRequired(), Length(6, 20)])
    verify = PasswordField("Verify Password", validators = [InputRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class AddItemForm(FlaskForm):
    title = StringField("Title", validators = [InputRequired()])
    author = StringField("Author", validators = [InputRequired()])
    description = TextField("Description", validators = [InputRequired()])
    isbn = isbn = IntegerField("ISBN", validators = [InputRequired()])
    price = FloatField("Price", validators = [InputRequired()])
    in_stock = IntegerField("# in stock", validators = [InputRequired()])
    location = TextField("Location", validators = [InputRequired()])

class SearchForm(FlaskForm):
    term = StringField("Search")
