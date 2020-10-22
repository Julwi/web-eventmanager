# __init__ is the starting point of a package structure
# Allows better structuring of imports and content

import os
from tempfile import mkdtemp

from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application (create instance of Flask)
app = Flask(__name__)

# Secret key for application (Security for client side session)
app.config["SECRET_KEY"] = "0888b3f10d30ae69a206e6d442a82e4b"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

# Configure bcrypt
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Configure Flask_APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Bottom imports to avoid circle import problems
# Routes import from app package too
# One directs to __init__.py with package name "app"
from app import routes