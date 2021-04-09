from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/post/new",  methods = ["GET", "POST"])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post had been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("createPost.html", title = "New Post", 
        form = form, legend = "New Post")

@posts.route("/post/<int:postID>",  methods = ["GET", "POST"])
def post(postID):
    post = Post.query.get_or_404(postID)
    return render_template("post.html", title = post.title, post = post)

@posts.route("/post/<int:postID>/update",  methods = ["GET", "POST"])
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
        return redirect(url_for("posts.post", postID = post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("createPost.html", title = "Update Post", 
        form = form, legend = "Update Post")

@posts.route("/post/<int:postID>/delete",  methods = ["POST"])
@login_required
def deletePost(postID):
    post = Post.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
