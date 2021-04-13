# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# # init SQLAlchemy so we can use it later in our models
# db = SQLAlchemy()
# from models import *

# def create_app():

#     app = Flask(__name__)
#     app.config.from_object(os.environ['APP_SETTINGS'])
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)

#     # blueprint for auth routes in our app
#     from .auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)

#     # blueprint for non-auth parts of app
#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     return app