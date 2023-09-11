from flask import Flask, render_template, request, redirect, url_for
from models import db, Task
from pony.orm import select, Database
from datetime import datetime
from pony.orm import db_session


app = Flask(__name__)

# Настройка подключения к PostgreSQL
app.config["DATABASE_URI"] = "postgres://viktorilin:postgres@localhost:5433/employee"


@app.route("/add_task", methods=["GET", "POST"])
@db_session
def add_task():
    if request.method == "POST":
        # Получаем данные из формы
        title = request.form.get("taskTitle")
        author = request.form.get("author")
        assignee = request.form.get("assignee")
        date = request.form.get("date")
        description = request.form.get("description")
        status = "Беклог"  # Устанавливаем начальный статус задачи

        # Создаем новую задачу и сохраняем ее в базу данных
        new_task = Task(
            title=title,
            author=author,
            assignee=assignee,
            date=date,
            description=description,
            status=status,
        )
        db.commit()  # Сохраняем изменения в базе данных
        return redirect(
            url_for("task_list")
        )  # Перенаправляем пользователя на список задач

    return render_template("add_task.html")  # Отображаем форму для добавления задачи


@app.route("/", methods=["GET", "POST"])
@db_session
def task_list():
    page = request.args.get("page", default=1, type=int)
    status = request.args.get("status", default=None, type=str)
    author = request.args.get("author", default=None, type=str)
    assignee = request.args.get("assignee", default=None, type=str)
    date = request.args.get("date", default=None, type=str)
    sort_option = request.args.get(
        "sort", default="dateAsc", type=str
    )  # Значение сортировки по умолчанию

    # Инициализируем пустой список задач
    tasks = []

    # Если есть параметры фильтрации, то выполняем фильтрацию
    if status or author or assignee or date:
        tasks_query = Task.select()  # Создаем запрос к базе данных

        # Фильтруем задачи на основе параметров
        if status:
            tasks_query = tasks_query.where(Task.status == status)
        if author:
            tasks_query = tasks_query.where(Task.author == author)
        if assignee:
            tasks_query = tasks_query.where(Task.assignee == assignee)
        if date:
            tasks_query = tasks_query.where(Task.date == date)

        # Применяем сортировку
        if sort_option == "dateAsc":
            tasks_query = tasks_query.order_by(Task.date)
        elif sort_option == "dateDesc":
            tasks_query = tasks_query.order_by(Task.date.desc())
        elif sort_option == "titleAsc":
            tasks_query = tasks_query.order_by(Task.title)
        elif sort_option == "titleDesc":
            tasks_query = tasks_query.order_by(Task.title.desc())

        # Получаем список задач из запроса
        tasks = list(tasks_query)

    # Производим пагинацию задач
    tasks_per_page = 10  # Количество задач на странице
    total_tasks = len(tasks)  # Общее количество задач

    pages = total_tasks // tasks_per_page
    if total_tasks % tasks_per_page > 0:
        pages += 1

    # Выбираем задачи для текущей страницы
    offset = (page - 1) * tasks_per_page
    tasks = tasks[offset : offset + tasks_per_page]

    return render_template("task_list.html", tasks=tasks, page=page, pages=pages)


if __name__ == "__main__":
    db.bind(
        provider="postgres",
        user="viktorilin",
        password="postgres",
        host="localhost",
        port=5433,
        database="viktorilin",
    )
    db.generate_mapping(create_tables=True)
    app.run(debug=True)
