from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////./database/inventory.db"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "JinUdceer0"

db = SQLAlchemy(app)

class Category(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
    app.run()
