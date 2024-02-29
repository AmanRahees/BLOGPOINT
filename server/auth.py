from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models.account import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    else:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash(message='Logged In', category="success")
                    return redirect(url_for("views.home"))
                else:
                    flash(message='Incorrect Password.', category="error")
            else:
                flash(message='User does not exist.', category="error")
        return render_template("pages/login.html", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(username, email, password, password2)
        isExists = User.query.filter_by(email=email).first()
        if isExists:
            flash(message='Email is already registered.', category="error")
        elif password != password2:
            flash(message='Password doesn\'t match.', category="error")
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(message='Registerd Successfully.', category="success")
            return redirect(url_for("views.home"))
    return render_template("pages/register.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))