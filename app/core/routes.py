# standard imports
from datetime import datetime

# flask imports
from flask import render_template

# from flask_wtf import Form
from flask_login import current_user, login_required

from app.core import bp
from app import db
from app.models import (
    User,
)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route("/")
@bp.route("/index")
def index():
    """
    Blablabla
    """
    if current_user.is_authenticated:
        payload = "Je bent authenticated"
    else:
        payload = "Je mag geen publieke dingen doen"
    return render_template("index.html", title="Home", payload=payload)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)