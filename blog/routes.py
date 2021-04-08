import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from blog import app, db, bcrypt, mail
from blog.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                        PostForm, RequestResetForm, ResetPasswordForm)
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(per_page = 2, page=page)
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash("Your account has successfully been created!", "success")
        return redirect(url_for("login"))
    return render_template('register.html', title = "Register Now", form = form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberMe.data)
            nextPage = request.args.get("next")
            return redirect(nextPage) if nextPage else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check login information.", "danger")
    return render_template('login.html', title = "Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def saveProfileImage(form_profileImage):
    randomHexVal = secrets.token_hex(8)
    fileName, fileExtension = os.path.splitext(form_profileImage.filename)
    imageFileName = randomHexVal + fileExtension
    imagePath = os.path.join(app.root_path, "static/pictures", imageFileName)
    outputSize = (250,250)
    newImage = Image.open(form_profileImage)
    newImage.thumbnail(outputSize)
    newImage.save(imagePath)
    return imageFileName


@app.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profileImage.data:
            imageFile = saveProfileImage(form.profileImage.data)
            current_user.imageFile = imageFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account information has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    imageFile = url_for("static", filename = "pictures/" + current_user.imageFile)
    return render_template('account.html', title = "Account Profile", imageFile = imageFile, form = form)

@app.route("/post/new",  methods = ["GET", "POST"])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post had been created!", "success")
        return redirect(url_for("home"))
    return render_template("createPost.html", title = "New Post", 
        form = form, legend = "New Post")

@app.route("/post/<int:postID>",  methods = ["GET", "POST"])
def post(postID):
    post = Post.query.get_or_404(postID)
    return render_template("post.html", title = post.title, post = post)

@app.route("/post/<int:postID>/update",  methods = ["GET", "POST"])
@login_required
def updatePost(postID):
    post = Post.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", postID = post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("createPost.html", title = "Update Post", 
        form = form, legend = "Update Post")

@app.route("/post/<int:postID>/delete",  methods = ["POST"])
@login_required
def deletePost(postID):
    post = Post.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))

@app.route("/user/<string:username>")
def userPosts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.datePosted.desc()).paginate(per_page = 1, page=page)
    return render_template("userPosts.html", posts=posts, user=user)

def sendResetEmail(user):
    token = user.get_reset_token()
    message = Message("Password Reset Request", 
                    sender = "noreply@demo.com", 
                    recipients=[user.email])
    message.body = f'''To reset your password, please visit the following link:
{url_for("resetToken", token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(message)

@app.route("/resetPassword", methods=["GET", "POST"])
def resetRequest():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetEmail(user)
        flash("A reset email has been sent to your email account.", "info")
        return redirect(url_for("login"))
    return render_template("resetRequest.html", title = "Reset Password", form = form)


@app.route("/resetPassword/<token>", methods=["GET", "POST"])
def resetToken(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid token received. The token is either invalid or expired.", "warning")
        return redirect(url_for("resetRequest"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashedPassword
        db.session.commit()
        flash("Your password has successfully been updated!", "success")
        return redirect(url_for("login"))
    return render_template("resetToken.html", title = "Reset Password", form = form)