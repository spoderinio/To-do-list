
from asyncio import all_tasks
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to-do-list.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_do = db.Column(db.String(250), unique=True, nullable=False)


db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    all_tasks = db.session.query(Task).all()

    return render_template("index.html", all_tasks=all_tasks)


@app.route("/add", methods=["POST"])
def add():
    data = request.form
    new_job = Task(to_do=data["new_task"])
    db.session.add(new_job)
    db.session.commit()
    return redirect("/")


@app.route("/remove_task", methods=["POST"])
def remove_task():
    all_tasks = db.session.query(Task).all()
    checked_boxes = request.form.getlist("check")
    print(checked_boxes)

    for item in range(len(checked_boxes)):
        idx = int(checked_boxes[item])
        if len(checked_boxes) > 1:
            item_to_delete = Task.query.filter_by(
                to_do=all_tasks[idx - 1].to_do).first()
            print(item_to_delete)
            db.session.delete(item_to_delete)
            db.session.commit()
        else:
            item_to_delete = Task.query.filter_by(
                to_do=all_tasks[0].to_do).first()
            print(item_to_delete)
            db.session.delete(item_to_delete)
            db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
