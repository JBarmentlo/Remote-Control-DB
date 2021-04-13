from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), primary_key=True)
    pas = db.Column(db.String())
    mail = db.Column(db.String())
    authenticated = db.Column(db.Boolean, default=False)

    # tasks = relationship("Task")
    
    def __init__(self, username, pas, mail, authenticated):
        self.username = username
        self.pas = pas
        self.mail = mail
        self.authenticated = authenticated

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the username to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return '<user {}>'.format(self.username)


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer(), primary_key = True)
    task = db.Column(db.String())
    username = db.Column(db.String())
    # user = db.Column(sb.String, ForeignKey('users.username'))

    def __init__(self, task_id, task, username):
        self.id = task_id
        self.task = task
        self.username = usernmame