from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import email_validator

app = Flask(__name__)   
app.config["SECRET_KEY"] = 'dcd7465c51c7a583e6fd4a605e00f590'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

#Import after initialization to avoid circular importing
from blog import routes