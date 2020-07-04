from .models import SessionLocal, Todo
from . import schemas


def task_todo_create(todo: schemas.Todo):
    db = SessionLocal()
    new_todo = Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.close()
