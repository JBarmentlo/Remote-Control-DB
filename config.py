import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_SCHLUSS"]


class ProductionConfig(Config):
    DEBUG = False
    try:
        SQLALCHEMY_DATABASE_URI = os.environ["DB_URL"]
    except:
        pass



class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://yup:paspas@localhost:5432/remotecontrol"



class TestingConfig(Config):
    TESTING = True