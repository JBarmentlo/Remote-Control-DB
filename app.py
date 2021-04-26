from init import *
from models import *
from server import *
from s3 import get_log_strings, create_obj
import datetime
from flask import send_from_directory

@login_manager.user_loader
def user_loader(username):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (username) user to retrieve

    """
    user = db.session.query(User).filter(User.username == username).first()
    return user


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.redirect(flask.url_for('upload'))

@app.route('/profilepic/<name>', methods=['GET', 'POST'])
def profilepic(name):
    create_obj(name + "_" + str(datetime.datetime.now()).split('.')[0])
    return send_from_directory('static', 'pic.jpg')
    

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":
        print(request.form)
        task = Task(None, request.form["text"], current_user.username)
        db.session.add(task)
        db.session.commit()
        return render_template('successful_upload.html', task=task)
    return render_template('upload.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if (user is None):
            return render_template('login.html', form=form)

        if (bcrypt.check_password_hash(user.pas, form.password.data)):
            print("Logged In")
            login_user(user)
            next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if next is not None and not is_safe_url(next, {os.environ["SAFE_HOSTS"]}):
                return flask.abort(400)
            flask.flash('Logged in successfully.')
            # db.session.commit()
            return flask.redirect(next or flask.url_for('upload'))
        else:
            print("NOPE")
        # db.session.commit()
    return render_template('login.html', form=form)


@app.route('/status')
@login_required
def status():
    tasks =  get_tasks_by_user(current_user)
    for task in tasks:
        task.set_run_time() 
    return render_template('status.html', tasks=tasks)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    errors = []
    if form.validate_on_submit():
        if (bcrypt.check_password_hash(b'$2b$12$H0im14vPWMOFm/bao3A1Neb4wXQsNisL4N3SRQl5WPCkuVazUIAWa', form.adminpas.data)):
            res = db.session.query(User).filter_by(username=form.username.data).first()
            if (res is not None):
                errors.append("Username already taken")
                return render_template('signup.html', form=form, error = errors)
            user = User(form.username.data, bcrypt.generate_password_hash(form.password.data), form.email.data)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                errors.append("Something went wrong with the database")
            print(f"user registered -{form.username.data}-")
            flask.flash('Thanks for registering')
            return redirect('/login')
        else:
            errors.append("Wrong adminpas")
    else:
        errors.append("Form invalid (maybe you didnt type the same password twice), username needs to be 4-25 chars long")
    return render_template('signup.html', form=form, error = errors)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")

@app.route("/details/<taskid>")
def details(taskid):
    task = get_task_by_id(taskid)
    out, err = get_log_strings(task.task_id)
    return render_template("detail.html", task = task, stdout = out, stderr = err)



if __name__ == '__main__':
    app.run()

@app.teardown_appcontext
def shutdown_session(*args, **kwargs):
    print("TEARDOOOOWN\n\n")
    # db.session.remove()

