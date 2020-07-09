from passlib.hash import pbkdf2_sha256

from .models import SessionLocal, Todo, User
from . import schemas


def task_user_create(user: schemas.User):
    db = SessionLocal()
    new_user = User(username=user.username,
                    password=pbkdf2_sha256.hash(user.password))
    db.add(new_user)
    db.commit()
    db.close()


def task_todo_create(todo: schemas.Todo):
    db = SessionLocal()
    new_todo = Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.close()
