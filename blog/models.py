#Imports defined here
from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin

#Returns User query based on given ID number.
@login_manager.user_loader
def load_user(userID):
    return User.query.get(int(userID))

#User class inherits from db.Model and UserMixIn from flask_login package
#Required Properties are: Username, email, ProfileImage, Password
#Additional property is posts, which has a relationship to the posts class, and a backreference
#to the User who created the posts.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    imageFile = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    #Here, posts references the Post class. Backref creats an attribute on a Post object
    #accessed by doing Post.author
    posts = db.relationship("Post", backref="author", lazy=True)

    #User is represented as User(Username, Email, ProfileImageFile)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.imageFile}')"

#Post class inherits from db.Model
#Required Properties are: ID, Title, DatePosted, Content, userID
#Additional property userID references the table of users in the database
#This property is needed for the posts relationship in the User class.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #Here, user.id references the user table and the id column.
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False) 

    #Post is represented as Post(Title, DatePosted)
    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"