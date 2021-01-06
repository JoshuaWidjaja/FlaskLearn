from flask import render_template, url_for, flash, redirect
from blog import app
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post

posts = [
    {
        "author": "Joshua Widjaja",
        "title": "Blog Post 1",
        "content": "First post",
        "datePosted": "December 23, 2020"
    },
    {
        "author": "Joe Mama",
        "title": "Blog Post 2",
        "content": "Second post",
        "datePosted": "January 1, 2020"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account Created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template('register.html', title = "Register Now", form = form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("Successful login!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check login information.", "danger")
    return render_template('login.html', title = "Login", form = form)
