from flask import render_template, request, redirect, url_for, Blueprint
from pony.orm import db_session

from database.models import db, Task


add = Blueprint("add", __name__)


@add.route("/add_task", methods=["GET", "POST"])
@db_session
def add_task():
    if request.method == "POST":
        title = request.form.get("taskTitle")
        author = request.form.get("author")
        assignee = request.form.get("assignee")
        date = request.form.get("date")
        description = request.form.get("description")
        status = "Беклог"

        new_task = Task(
            title=title,
            author=author,
            assignee=assignee,
            date=date,
            description=description,
            status=status,
        )
        db.commit()
        return redirect(url_for("main.main_page"))

    return render_template("add_task.html")
