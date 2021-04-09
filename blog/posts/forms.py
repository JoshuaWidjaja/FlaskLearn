from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

#Post Form defined here. Called when user creates a new post or edits an existing one
#By default, if editing, fields are populated with current post information.
#Required fields are: Title, Content
#Submit button added at the bottom.
class PostForm(FlaskForm):
    title = StringField("Title", validators= [DataRequired()])
    content = TextAreaField("Content", validators= [DataRequired()])
    submit = SubmitField("Post")