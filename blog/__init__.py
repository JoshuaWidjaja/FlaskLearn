from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import email_validator

app = Flask(__name__)   
app.config["SECRET_KEY"] = 'dcd7465c51c7a583e6fd4a605e00f590'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from blog import routes