from flask import render_template, request, Blueprint
from database.models import Task
from pony.orm import select, db_session, desc


sort = Blueprint("sort", __name__)


@sort.route("/apply_sort", methods=["POST"])
@db_session
def apply_sort():
    sort_option = request.form.get("sort_option")

    total_tasks = 0

    if sort_option == "dateAsc":
        tasks = Task.select().order_by(Task.created_at)
        total_tasks = len(tasks)
    elif sort_option == "dateDesc":
        tasks = Task.select().order_by(desc(Task.created_at))
        total_tasks = len(tasks)
    elif sort_option == "titleAsc":
        tasks = Task.select().order_by(Task.title)
        total_tasks = len(tasks)
    elif sort_option == "titleDesc":
        tasks = Task.select().order_by(desc(Task.title))
        total_tasks = len(tasks)
    else:
        tasks = Task.select()

    return render_template(
        "task_list.html",
        tasks=tasks,
        selected_sort_option=sort_option,
        total_tasks=total_tasks,
    )
