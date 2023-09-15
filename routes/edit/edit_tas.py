from flask import render_template, request, redirect, url_for, Blueprint
from database.models import db, Task
from pony.orm import db_session


edit_t = Blueprint("edit_t", __name__)


@edit_t.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@db_session
def edit_task(task_id):
    task = Task.get(id=task_id)

    if request.method == "POST":
        task.title = request.form.get("taskTitle")
        task.author = request.form.get("author")
        task.assignee = request.form.get("assignee")
        task.description = request.form.get("description")
        task.status = request.form.get("status")

        db.commit()
        return redirect(url_for("main.main_page"))

    return render_template("edit_task.html", task=task)
