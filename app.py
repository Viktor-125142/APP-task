from flask import Flask

from database.models import db
from routes.edit.edit_tas import edit_t
from routes.main_page.main_page import main
from routes.add_task.add_task import add
from routes.filter.filter import filter
from routes.filter.sort import sort
from routes.buttons_del_edit_form.perform_action import butt_del_edit

app = Flask(__name__)

# Настройка подключения к PostgreSQL
app.config["DATABASE_URI"] = "postgres://viktorilin:postgres@localhost:5433/employee"

db.bind(
    provider="postgres",
    user="viktorilin",
    password="postgres",
    host="localhost",
    port=5433,
    database="viktorilin",
)
db.generate_mapping(create_tables=True)

# Роутер который обрабатывает запрос отображения на главной странице
app.register_blueprint(main)

# Отобрабатывает форму для добавления задачи
app.register_blueprint(add)

# Роутер который обрабатывает запрос на изменение задачи
app.register_blueprint(edit_t)

# обрабатывает фильтр на главной странице
app.register_blueprint(filter)

# Обрабатывает сортировку на странице
app.register_blueprint(sort)

app.register_blueprint(butt_del_edit)


if __name__ == "__main__":
    app.run(debug=True)
