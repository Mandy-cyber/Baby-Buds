from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint("auth", __name__)

# user login
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # an existing account with the given email, or None
        user = email_exists(email)

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.forum'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

# expert signup
@auth.route("/sign-up-expert", methods=["GET", "POST"])
def sign_up_expert():
    if request.method == 'POST':
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # TODO abstract input validation
        if email_exists(email):
            flash('Email is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:  # TODO add further email validation
            flash("Email is invalid.", category='error')
        else:
            new_expert = User(email=email,
                              username=first_name+" "+last_name,
                              password=generate_password_hash(password1, method='sha256'),
                              is_parent=False)

        db.session.add(new_expert)
        db.session.commit()
        login_user(new_expert, remember=True)
        flash('Expert account created!')
        return redirect(url_for('views.forum'))

    return render_template("signup_expert.html", user=current_user)

# parent signup
@auth.route("/sign-up-mom", methods=["GET", "POST"])
def sign_up_mom():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # TODO abstract input validation
        if email_exists(email):
            flash('Email is already in use.', category='error')
        if username_exists(username):
            flash('Username already exists.', category='error')
        if password1 != password2:
            flash('Password don\'t match!', category='error')
        if len(username) < 2:
            flash('Username is too short.', category='error')
        if len(password1) < 6:
            flash('Password is too short.', category='error')
        if len(email) < 4:  # TODO add further email validation
            flash("Email is invalid.", category='error')

        new_parent = User(email=email,
                          username=username,
                          password=generate_password_hash(password1, method='sha256'),
                          is_parent=True)
        db.session.add(new_parent)
        db.session.commit()
        login_user(new_parent, remember=True)
        flash('Parent Account Created!')
        return redirect(url_for('views.forum'))

    return render_template("signup_mom.html", user=current_user)

# logout - redirects to Forum home
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.forum"))

# ------------------------------------------------------------------------
# VALIDATION HELP
# ------------------------------------------------------------------------

# returns the user associated with the given email, if one exists
# None otherwise
def email_exists(email):
    return User.query.filter_by(email=email).first()

# returns the user associated with the given username, if one exists
# None otherwise
def username_exists(username):
    return User.query.filter_by(username=username).first()
