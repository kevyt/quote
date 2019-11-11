# flask imports
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

from flask_login import current_user, login_user, logout_user, login_required

from app import db

from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Route processing login
    If endpoint for which authentication is needed was hit first,
    user will be referred to that endpoint after login
    """
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Ongeldige gebruikersnaam of wachtwoord")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("core.index")
        if 'quote_id' in request.args:
            next_page = url_for("core.index", quote_id=request.args['quote_id'], image_id=request.args['image_id'])
        return redirect(next_page)

    return render_template("login.html", title="Aanmelden", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Route to register user
    If user is already authenticated, user will be referred to index
    Otherwise, form will be displayed
    On registration password will be hashed
    On succesful registration, user will be referred to login page
    """
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Succesvol geregistreerd")
        return redirect(url_for("auth.login"))
    return render_template("login.html", title="Register", form=form)
