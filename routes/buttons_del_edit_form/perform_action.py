from flask import request, redirect, url_for, Blueprint
from database.models import Task
from pony.orm import db_session

butt_del_edit = Blueprint("butt_del_edit", __name__)


@butt_del_edit.route("/perform_action", methods=["POST"])
@db_session
def perform_action():
    selected_action = request.form.get("selected_action")

    if selected_action == "edit":
        task_id = request.form.get("task_id")
        return redirect(f"/edit_task/{task_id}")

    elif selected_action == "delete":
        task_id = request.form.get("task_id")
        task = Task.get(id=task_id)
        if task:
            task.delete()

    return redirect(url_for("main.main_page"))
