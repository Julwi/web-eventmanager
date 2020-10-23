from datetime import datetime
from time import localtime, strptime, strftime
import queue

from flask import flash, url_for, redirect, render_template, request, session, abort, current_app
from app import app, bcrypt, db
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required

# Event validation variables
events_completedq = queue.Queue()
basis_seconds = datetime(1970, 1, 1)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("overview"))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash password and add user to db
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Flash for sending messages in Flask; First argument is message, second a category (optional)
        flash(
            f"Account for {form.username.data} was created. You can login now!", "success")
        return redirect(url_for("login"))

    else:
        return render_template("register.html", title="Register", form=form)


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

            # if user tried to access a forbidden page before login there is a next argument added
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("overview"))

        else:
            flash("Login failed. Please check username and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/overview", methods=["GET"])
@login_required
def overview():
    events = Event.query.filter_by(user_id=current_user.id)

    # Process completed events
    if not events_completedq.empty():
        event_id = int(events_completedq.get())
        app.apscheduler.remove_job(str(event_id))
        print("removed job with id {}." .format(event_id))
        events_completedq.task_done()
    
    # Check if any events are completed
    # Move event into archive
    # Display alarm 


    current_jobs = app.apscheduler.get_jobs()
    for event in events:

        # Check if job is already running
        job_running = False
        for job in current_jobs:
            if job.name == str(event.id):
                job_running = True
                continue

        # Continue or create job check_date for event
        if job_running:
            break
        app.apscheduler.add_job(func=check_date, trigger='cron', minute='*', args=[
                                event.id, event.date_eventdatetime], id=str(event.id))

    return render_template("overview.html", title="Overview", events=events)


def check_date(event_id, event_datetime):
    """
    Scheduled function to check event date every minute. 
    Passes the event id to global queue if event is completed.

    Parameters:
    event_id (str): Event id of respective event as a string.
    event_datetime (datetime.datetime): Scheduled datetime of event. 
    """
    completed = False

    # Get current time
    current_datetime = strftime("%m/%d/%Y %I:%M %p", localtime())
    time_current = datetime.strptime(current_datetime, "%m/%d/%Y %I:%M %p")

    # Check if event is in the past
    if (time_current-basis_seconds).total_seconds() > (event_datetime-basis_seconds).total_seconds():
        completed = True
        events_completedq.put(event_id)

    # Status
    print("Job for event id {} is alive. Event completed: {}." .format(
        event_id, completed))


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = EventForm()

    # If entered values are valid commit event to db
    if form.validate_on_submit():
        event = Event(title=form.title.data,
                      date_eventdatetime=datetime.strptime(
                          form.eventdatetime.data, "%m/%d/%Y %I:%M %p"),
                      description=form.description.data,
                      user_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        flash("Your event has been created!", "success")
        return redirect(url_for("overview"))

    form.submit.label.text = 'Create'
    return render_template("create.html", title="Create Event", form=form, legend="Create Your Next Event!")


@app.route("/update/<int:event_id>", methods=["GET", "POST"])
@login_required
def update(event_id):
    # Query event from db and check if user is author
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    form = EventForm()

    # If entered values are valid commit changes to db
    if form.validate_on_submit():
        event.title = form.title.data
        event.date_eventdatetime = datetime.strptime(
            form.eventdatetime.data, "%m/%d/%Y %I:%M %p")
        event.description = form.description.data
        db.session.commit()
        flash("Your event has been updated!", "success")
        return redirect(url_for("overview"))

    # Fill form with event data from db
    if request.method == "GET":
        form.title.data = event.title
        form.eventdatetime.data = event.date_eventdatetime.strftime(
            "%m/%d/%Y %I:%M %p")
        form.description.data = event.description
        form.submit.label.text = 'Update'
    return render_template("update.html", title="Update Event", event=event, form=form, legend="Update Post")


@app.route("/delete/<int:event_id>", methods=["POST"])
@login_required
def delete(event_id):
    # Query event from db and check if user is author
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    db.session.delete(event)
    db.session.commit()
    flash("Event has been deleted", "success")
    return redirect(url_for("overview"))


@app.route("/archive")
@login_required
def archive():
    return render_template("archive.html", title="Register")
