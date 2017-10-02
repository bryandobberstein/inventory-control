from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from werkzeug import generate_password_hash, check_password_hash
from forms import TestForm, LoginForm, RegisterForm, AddItemForm

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
lm = LoginManager(app)
bootstrap = Bootstrap(app)

from views import *

lm.login_view = "login"

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == "__main__":
    app.run()
