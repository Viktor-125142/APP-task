from flask import render_template, Blueprint
from database.models import Task
from pony.orm import select, db_session


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@db_session
def main_page():
    tasks = Task.select()[:]

    total_tasks = len(tasks)

    return render_template(
        "task_list.html",
        tasks=tasks,
        total_tasks=total_tasks,
    )
