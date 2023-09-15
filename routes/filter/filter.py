from flask import render_template, request, Blueprint, redirect, url_for
from database.models import Task
from pony.orm import select, db_session


filter = Blueprint("filter", __name__)


@filter.route("/apply_filter", methods=["GET", "POST"])
@db_session
def apply_filter():
    status = request.form.get("status")
    author = request.form.get("author")
    assignee = request.form.get("assignee")
    date = request.form.get("date")

    if not (status or author or assignee or date):
        return redirect(url_for("main.main_page"))

    page = int(request.args.get("page", 1))

    tasks_query = Task.select()

    filters = []

    if status:
        filters.append(Task.status == status)
    if author:
        filters.append(Task.author == author)
    if assignee:
        filters.append(Task.assignee == assignee)
    if date:
        filters.append(Task.date == date)

    final_filter = None

    if filters:
        final_filter = filters[0]
        for filter_condition in filters[1:]:
            final_filter &= filter_condition

    if final_filter:
        tasks_query = tasks_query.where(final_filter)

    tasks = list(tasks_query)

    total_tasks = Task.select().count()

    tasks_per_page = 5
    start_index = (page - 1) * tasks_per_page
    end_index = page * tasks_per_page

    tasks = tasks[start_index:end_index]

    return render_template(
        "task_list.html",
        tasks=tasks,
        selected_status=status,
        total_tasks=total_tasks,
    )
