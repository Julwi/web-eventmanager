# Database Models
# SQLAlchemy is an object-relational mapper (ORM); maps objects with db

from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Additional query in the background that connects user with events
    events = db.relationship('Event', backref="author", lazy=True)

    def __repr__(self):
        """ Define print format for user """
        return f"User('{self.username}', '{self.email}')"


class Event (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, default="Event")
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    date_eventdatetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """ Define print format for event """
        return f"Event('{self.title}', '{self.date_created}', '{self.date_eventdatetime}')"
