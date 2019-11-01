from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
)

from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Gebruikernaam", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    password2 = PasswordField(
        "Herhaal wachtwoord", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Verstuur")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Gebruik een andere gebruikersnaam")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Gebruik een ander e-mailadres")


class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired()])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    remember_me = BooleanField("Vergeet me niet")
    submit = SubmitField("Inloggen")
