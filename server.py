from init import db
from models import *


def get_all_tasks(limit = 100):
    tasks = db.session.query(Task).order_by(Task.date.desc()).limit(limit).all()
    try:
        for task in tasks:
            task.set_run_time
    except:
        pass
    return tasks


def get_tasks_by_user(user, limit = 20):
    tasks = db.session.query(Task).order_by(Task.date.desc()).limit(limit).all()
    try:
        for task in tasks:
            task.set_run_time
    except:
        pass
    return tasks


def get_task_by_id(id):
    task = db.session.query(Task).filter(Task.task_id == id).first()
    try:
        task.set_run_time()
    except:
        pass
    return task
