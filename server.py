from app import db


def get_all_tasks(limit = 100):
    return db.session.query(Task).order_by(Task.date.desc()).limit(limit).all()

def get_tasks_by_user(user, limit = 20):
    return db.session.query(Task).order_by(Task.date.desc()).limit(limit).all()

def get_taks_by_id(id):
    return db.session.query(Task).filter(Task.task_id == id).limit(limit).first()
