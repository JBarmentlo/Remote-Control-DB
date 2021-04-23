from flask import Flask, render_template, redirect, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
import flask
from is_safe_url import is_safe_url
import logging 
# from sqlalchemy import text, engine
# from sqlalchemy.orm import sessionmaker, scoped_session

# Session = scoped_session(session_factory)
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
login_manager.login_view = 'login'