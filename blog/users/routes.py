from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                            RequestResetForm, ResetPasswordForm)
from blog.users.utils import saveProfileImage, sendResetEmail

users = Blueprint("users", __name__)

@users.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash("Your account has successfully been created!", "success")
        return redirect(url_for("users.login"))
    return render_template('register.html', title = "Register Now", form = form)

@users.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberMe.data)
            nextPage = request.args.get("next")
            return redirect(nextPage) if nextPage else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check login information.", "danger")
    return render_template('login.html', title = "Login", form = form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods = ["GET", "POST"])
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
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    imageFile = url_for("static", filename = "pictures/" + current_user.imageFile)
    return render_template('account.html', title = "Account Profile", imageFile = imageFile, form = form)


@users.route("/user/<string:username>")
def userPosts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.datePosted.desc()).paginate(per_page = 1, page=page)
    return render_template("userPosts.html", posts=posts, user=user)

@users.route("/resetPassword", methods=["GET", "POST"])
def resetRequest():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetEmail(user)
        flash("A reset email has been sent to your email account.", "info")
        return redirect(url_for("users.login"))
    return render_template("resetRequest.html", title = "Reset Password", form = form)


@users.route("/resetPassword/<token>", methods=["GET", "POST"])
def resetToken(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid token received. The token is either invalid or expired.", "warning")
        return redirect(url_for("users.resetRequest"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashedPassword
        db.session.commit()
        flash("Your password has successfully been updated!", "success")
        return redirect(url_for("users.login"))
    return render_template("resetToken.html", title = "Reset Password", form = form)    