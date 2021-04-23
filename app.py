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


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
login_manager.login_view = 'login'

from models import *

@login_manager.user_loader
def user_loader(username):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (username) user to retrieve

    """
    print ("user_LOADER")
    user = User.query.get(username)
    return user

def get_new_task_id():
    last_task = db.session.query(Task).filter(Task.task_id == db.session.query(func.max(Task.task_id))).first()
    db.session.expunge(last_task)
    if (last_task is not None):
        last_id = last_task.task_id + 1
    else:
        last_id = 0
    return last_id

@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.redirect(flask.url_for('upload'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":
        print(request.form)
        task = Task(get_new_task_id(), request.form["text"], current_user.username)
        db.session.add(task)
        db.session.commit()
        return render_template('successful_upload.html', task=task)
    return render_template('upload.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User.query.filter_by(username=form.username.data).first()
        if (user is None):
            return render_template('login.html', form=form)

        if (bcrypt.check_password_hash(user.pas, form.password.data)):
            print("Logged In")
            login_user(user)
            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if next is not None and not is_safe_url(next, {os.environ["SAFE_HOSTS"]}):
                return flask.abort(400)
            flask.flash('Logged in successfully.')
            db.session.remove()
            return flask.redirect(next or flask.url_for('upload'))
        else:
            print("NOPE")
        db.session.remove()
    return render_template('login.html', form=form)


@app.route('/status')
@login_required
def status():
    tasks =  Task.query.filter_by(username=current_user.username).all()
    return render_template('status.html', tasks=tasks)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    errors = []
    if form.validate_on_submit():
        if (bcrypt.check_password_hash(b'$2b$12$H0im14vPWMOFm/bao3A1Neb4wXQsNisL4N3SRQl5WPCkuVazUIAWa', form.adminpas.data)):
            res = User.query.filter_by(username=form.username.data).first()
            if (res is not None):
                errors.append("Username already taken")
                return render_template('signup.html', form=form, error = errors)
            user = User(form.username.data, bcrypt.generate_password_hash(form.password.data), form.email.data)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                errors.append("Something went wrong with the database")
            print(f"user registered -{form.username.data}-")
            flask.flash('Thanks for registering')
            return redirect('/login')
        else:
            errors.append("Wrong adminpas")
    else:
        errors.append("Form invalid (maybe you didnt type the same password twice), username needs to be 4-25 chars long")
    return render_template('signup.html', form=form, error = errors)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")

if __name__ == '__main__':
    app.run()

@app.teardown_appcontext
def shutdown_session(*args, **kwargs):
    print("TEARDOOOOWN\n\n")
    # db.session.remove()