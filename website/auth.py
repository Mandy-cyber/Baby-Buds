from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Mom, Expert
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        user_type = request.form.get("user_type")
        password = request.form.get("password")

        if user_type == 'Expert':
            user = Expert.query.filter_by(email=email).first()
        else:
            user = Mom.query.filter_by(email=email).first()

        if email_in_use(email):
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.forum'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route("/sign-up-expert", methods=["GET", "POST"])
def sign_up_expert():
    if request.method == 'POST':
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if email_in_use(email):
            flash('Email is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            new_expert = Expert(email=email, first_name=first_name,
                                last_name=last_name, password=generate_password_hash(
                                    password1, method='sha256'))

            db.session.add(new_expert)
            db.session.commit()
            login_user(new_expert, remember=True)
            flash('Expert account created!')
            return redirect(url_for('views.forum'))

    return render_template("signup_expert.html", user=current_user)


@auth.route("/sign-up-mom", methods=["GET", "POST"])
def sign_up_mom():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        username_exists = Mom.query.filter_by(username=username).first()

        if email_in_use(email):
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            new_mom = Mom(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_mom)
            db.session.commit()
            login_user(new_mom, remember=True)
            flash('Mom Account Created!')
            return redirect(url_for('views.forum'))

    return render_template("signup_mom.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.forum"))


def email_in_use(email):
    expert_exists = Expert.query.filter_by(email=email).first()
    mom_exists = Mom.query.filter_by(email=email).first()

    return expert_exists or mom_exists
