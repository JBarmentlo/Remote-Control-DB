
# def get_new_task_id():
#     last_task = db.session.query(Task).filter(Task.task_id == db.session.query(func.max(Task.task_id))).first()
#     if (last_task is not None):
#         last_id = last_task.task_id + 1
#     else:
#         last_id = 0
#     db.session.commit()
#     return last_id