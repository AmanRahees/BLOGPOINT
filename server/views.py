from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from . import db
from .models.posts import Posts

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    posts = Posts.query.all()
    context = {
        "user": current_user,
        "posts": posts
    }
    return render_template("pages/index.html", **context)

@views.route("/create-post", methods=["GET", "POST"])
def create_post():
    if current_user.is_authenticated:
        if request.method == "POST":
            text = request.form.get("text")
            if not text:
                flash(message="Post cannot be empty", category="error")
            else:
                post = Posts(text=text, author=current_user.id)
                db.session.add(post)
                db.session.commit()
                flash(message="Post Created!", category="success")
                return redirect(url_for("views.home"))
        return render_template("pages/create_post.html", user=current_user)
    else:
        return redirect(url_for("views.home"))
    

@views.route("/delete-post/<int:id>")
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if post.author == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")
    else:
        flash("You are not authorized to delete this post", "danger")
    return redirect(url_for("views.home"))