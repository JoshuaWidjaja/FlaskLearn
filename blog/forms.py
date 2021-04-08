#Imports defined here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User
import email_validator

#Registration Form defined here. Called when registering for a new account.
#Required fields are: Username, email, password, confirm password
#Submit field added at the bottom
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #Below are checks to see if duplicate username/emails exist.
    #Flask checks for extra functions with the pattern "validate_(fieldname)" 
    #and calls these functions within the FlaskForm class
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken. Please choose another one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already taken. Please choose another one.")

#Login Form defined here. Called when logging in to an already existing user.
#Required fields are: Email, Password
#Nonrequired fields are Remember me button
#Submit field added at the bottom
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Login')

#Update Account Form defined here. Called when updating personal account information.
#By default, fields will be populated with current account information
#Required fields are: Username, email
#Nonrequired fields are Profile Image
#Submit field added at the bottom
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email() ])
    profileImage = FileField("Update Profile Picture", validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Account')

    #Flask checks for extra functions with the pattern "validate_(fieldname)" 
    #and calls these functions within the FlaskForm class.
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken. Please choose another one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email is already taken. Please choose another one.")

#Post Form defined here. Called when user creates a new post or edits an existing one
#By default, if editing, fields are populated with current post information.
#Required fields are: Title, Content
#Submit button added at the bottom.
class PostForm(FlaskForm):
    title = StringField("Title", validators= [DataRequired()])
    content = TextAreaField("Content", validators= [DataRequired()])
    submit = SubmitField("Post")

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No account exists with the given email. Please register for an account.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")