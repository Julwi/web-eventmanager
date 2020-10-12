from flask import flash, url_for, redirect, render_template, request, session
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required

@app.after_request
# Ensure responses aren't cached
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("overview"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("overview"))

    form = LoginForm()

    if form.validate_on_submit():

        # User-Login
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("overview"))

        else:
            flash("Login failed. Please check username and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("overview"))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Hash password and add user to db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User (username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Flash for sending messages in Flask; First argument is message, second a category (optional)
        flash(f"Account for {form.username.data} was created. You can login now!", "success")
        return redirect(url_for("login"))

    else:
        return render_template("register.html", title="Register", form=form)


@app.route("/overview")
@login_required
def overview():
    return render_template("overview.html", title="Overview")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = EventForm()

    if form.validate_on_submit():
        # TODO: Create Event
        print("TODO")

    return render_template("create.html", title="Create Event", form=form)


@app.route("/archive")
@login_required
def archive():    
    return render_template("archive.html", title="Register")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))