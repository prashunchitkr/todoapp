from typing import List

from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models
from . import schemas
from .models import SessionLocal, engine
from .tasks import task_todo_create

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ("http://localhost:3000" "http://localhost:8080")

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=['*'],
                   allow_headers=['*'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/todos')
def get_todos(
    request: Request, db: Session = Depends(get_db)) -> List[schemas.Todo]:
    '''
    Returns all the todos available in the database
    '''
    todos = db.query(models.Todo).all()
    return todos


@app.post('/todos')
async def create_todo(
    todo: schemas.TodoPost,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> schemas.Todo:
    '''
    Creates a todo item and adds it to the dictionary
    '''
    background_tasks.add_task(task_todo_create, todo)
    return todo


@app.delete('/todos/{id}')
async def delete_todo(id: int, db: Session = Depends(get_db)):
    '''
    Delete a model from the database
    '''
    q = db.query(models.Todo).get(id)
    if q.first():
        q.delete()
        db.commit()
        return {'code': 'success'}
    return {'code': 'error'}


@app.put('/todos/{id}')
async def update_todo(id: int,
                      todo: schemas.TodoPost,
                      db: Session = Depends(get_db)):
    '''
    Update the object in database
    '''
    q = db.query(models.Todo).filter(models.Todo.id == id)

    if q.first():
        q.update(todo.dict())
        db.commit()
        return {'code': 'success'}

    return {'code': 'error'}
