from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    # """ User Class """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    imageFile = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    #Here, Post references the Post class
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.imageFile}')"
        
class Post(db.Model):
    # Post Class
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #Here, user.id references the user table and the id column.
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False) 

    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"