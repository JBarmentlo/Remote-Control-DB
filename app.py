from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
from models import *


@app.route('/')
def hello():
    return "Hello World!"


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (username) user to retrieve

    """
    return User.query.get(user_id)

# @app.route('/')
# @login_required
# def hello():
#     return "Hello World!"


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

# if __name__ == '__main__':
#     app.run()