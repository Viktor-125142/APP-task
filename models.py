from pony.orm import Database, Required, Optional
from datetime import datetime

db = Database()


class Task(db.Entity):
    title = Required(str)
    author = Required(str)
    assignee = Required(str)
    created_at = Required(datetime, default=datetime.utcnow)
    description = Optional(str)
    status = Required(str)
    date = Required(datetime)
