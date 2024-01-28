from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    weight_user = db.Column(db.Integer, nullable=True)
    complete = db.Column(db.Boolean, default=False)


@app.route('/')
def hello_world():
    tasks = Tasks.query.all()
    return render_template('base.html', tasks=tasks)

@app.route('/user_tasks')
def user_tasks():
    task_list = Tasks.query.all()
    return render_template("add_tasks.html", task_list=task_list)


@app.route('/add_task', methods = ["POST"])
def add_task():
    title = request.form.get("title")
    deadline_str = request.form.get("deadline")
    deadline = datetime.strptime(deadline_str,'%Y-%m-%d') if deadline_str else None
    weight_user = request.form.get("weight", type=int)
    new_task = Tasks(title=title, weight_user=weight_user, deadline=deadline,complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')


@app.route("/update/<int:task_id>")
def update(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        task.complete = not task.complete
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
