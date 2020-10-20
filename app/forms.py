# Define forms for application
from datetime import datetime
from time import localtime, strftime, strptime

import flask_wtf
from flask_wtf import FlaskForm, Form
from wtforms import BooleanField, PasswordField, StringField, TextAreaField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

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
    title = StringField("Eventname", validators=[
                        DataRequired()], render_kw={'autofocus': True})
    eventdatetime = StringField("Eventdate", validators=[DataRequired(),
                                                        Regexp('\d\d/\d\d/\d\d\d\d\s((1[0-2]:[0-5]\d\s)|[1-9]:[0-5]\d\s)[A,P]M$', 
                                                        message="Use format mm/dd/yyyy hh:mm AM/PM")],
                                                        render_kw={'data-target': "#datetimepicker"})
    description = TextAreaField("Description")
    submit = SubmitField()

    def validate_eventdatetime(self, eventdatetime):
        basis_seconds = datetime(1970, 1, 1)
        current_datetime = strftime("%m/%d/%Y %I:%M %p", localtime())
        time_current = datetime.strptime(current_datetime, "%m/%d/%Y %I:%M %p")
        time_event = datetime.strptime(
            str(eventdatetime.data), "%m/%d/%Y %I:%M %p")

        # if event lies in the past (less total seconds than current time stamp)
        if (time_current-basis_seconds).total_seconds() > (time_event-basis_seconds).total_seconds():
            raise ValidationError("Event must be in the future.")
