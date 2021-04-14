from flask import Flask, render_template, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
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
    return User.query.get(username)

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        print(bcrypt.generate_password_hash(form.username.data))
        print(form.username.data)
        print(form.password.data)
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        print(user.pas)
        if (user is None):
            return render_template('login.html', form=form)

        if (bcrypt.check_password_hash(user.pas, form.password.data)):
            print("Logged In")
            login_user(user)
            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)
            flask.flash('Logged in successfully.')
            return flask.redirect(next or flask.url_for('index'))

        else:
            print("NOPE")


    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        if (bcrypt.check_password_hash(b'$2b$12$H0im14vPWMOFm/bao3A1Neb4wXQsNisL4N3SRQl5WPCkuVazUIAWa', form.adminpas.data)):
            res = User.query.filter_by(username=form.username.data).first()
            if (res is not None):
                return render_template('signup.html', form=form, error = "Username already taken")
            user = User(form.username.data, bcrypt.generate_password_hash(form.password.data), form.email.data)
            db.session.add(user)
            db.session.commit()
            print(f"user registered -{form.username.data}-  -{form.password.data}-")
        flask.flash('Thanks for registering')
        return redirect('/login')
    return render_template('signup.html', form=form, error = "")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """For GET requests, display the login form. 
#     For POSTS, login the current user by processing the form.

#     """
#     # print db
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.get(form.email.data)
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 user.authenticated = True
#                 db.session.add(user)
#                 db.session.commit()
#                 login_user(user, remember=True)
#                 return redirect(url_for("bull.reports"))
#     return render_template("login.html", form=form)

# @app.route("/logout", methods=["GET"])
# @login_required
# def logout():
#     """Logout the current user."""
#     user = current_user
#     user.authenticated = False
#     db.session.add(user)
#     db.session.commit()
#     logout_user()
#     return render_template("logout.html")

if __name__ == '__main__':
    app.run()