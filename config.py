import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL_2']
    except:
        print("NO SQL DB URI")
        SQLALCHEMY_DATABASE_URI = "fuck"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:suki@localhost:5432/resbot_dev"


class TestingConfig(Config):
    TESTING = True