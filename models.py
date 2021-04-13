from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), primary_key=True)
    pas = db.Column(db.String())
    mail = db.Column(db.String())
    # tasks = relationship("Task")
    
    def __init__(self, username, pas, mail):
        self.username = username
        self.pas = pas
        self.mail = mail
        
    def __repr__(self):
        return '<user {}>'.format(self.user)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key = True)
    task = db.column(db.String())
    username = db.Column(db.String())
    # user = db.Column(sb.String, ForeignKey('users.username'))

    def __init__(self, id, task, username):
        self.id = id
        self.task = task
        self.username = usernmame