# Define forms for application

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=3, max=20)], render_kw={'autofocus': True})
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField("Confirm Password", validators=[
                            DataRequired(), EqualTo("password", message='Passwords must match')])
    submit = SubmitField("Sign up")

    # Custom validation (does username already exist)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken. Try different one.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=3, max=20)], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class EventForm(FlaskForm):
    title = StringField("Eventname", render_kw={'autofocus': True})
    eventdatetime = DateTimeField("Eventdate")
    submit = SubmitField("Create")
