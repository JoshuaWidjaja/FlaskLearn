import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail

def saveProfileImage(form_profileImage):
    randomHexVal = secrets.token_hex(8)
    fileName, fileExtension = os.path.splitext(form_profileImage.filename)
    imageFileName = randomHexVal + fileExtension
    imagePath = os.path.join(current_app.root_path, "static/pictures", imageFileName)
    outputSize = (250,250)
    newImage = Image.open(form_profileImage)
    newImage.thumbnail(outputSize)
    newImage.save(imagePath)
    return imageFileName

def sendResetEmail(user):
    token = user.get_reset_token()
    message = Message("Password Reset Request", 
                    sender = "noreply@demo.com", 
                    recipients=[user.email])
    message.body = f'''To reset your password, please visit the following link:
{url_for("users.resetToken", token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(message)