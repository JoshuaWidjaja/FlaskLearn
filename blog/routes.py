import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")

@app.route("/home")
def home():
    posts = Post.query.all()
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