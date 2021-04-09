import os

class Config:
    SECRET_KEY = os.environ.get("FLASKLEARN_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASKLEARN_DATABASE_URI")
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    #app.config["MAIL_USER_TLS"] = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")