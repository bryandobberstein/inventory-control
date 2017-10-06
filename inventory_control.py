from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
lm = LoginManager(app)
bootstrap = Bootstrap(app)

from views import *

lm.login_view = "login"

if __name__ == "__main__":
    app.run()
