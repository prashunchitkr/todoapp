from typing import List

from fastapi import BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas
from .app import app, get_db
from .tasks import task_todo_create, task_user_create
from .auth import get_current_user, authenticate_user, create_access_token, oauth2_scheme


@app.get('/todos')
def get_todos(db: Session = Depends(get_db),
              user: models.User = Depends(get_current_user)) -> List[
                  schemas.Todo]:
    '''
    Returns all the todos available in the database
    '''
    todos = db.query(models.Todo).all()
    return todos


@app.post('/todos')
async def create_todo(
    todo: schemas.TodoPost,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
) -> schemas.Todo:
    '''
    Creates a todo item and adds it to the dictionary
    '''
    background_tasks.add_task(task_todo_create, todo)
    return todo


@app.delete('/todos/{id}')
async def delete_todo(id: int,
                      db: Session = Depends(get_db),
                      user: models.User = Depends(get_current_user)):
    '''
    Delete a model from the database
    '''
    q = db.query(models.Todo).get(id)
    if q:
        db.delete(q)
        db.commit()
        return {'code': 'success'}
    return {'code': 'error'}


@app.put('/todos/{id}')
async def update_todo(id: int,
                      todo: schemas.TodoPost,
                      db: Session = Depends(get_db),
                      user: models.User = Depends(get_current_user)):
    '''
    Update the object in database
    '''
    q = db.query(models.Todo).filter(models.Todo.id == id)

    if q.first():
        q.update(todo.dict())
        db.commit()
        return {'code': 'success'}

    return {'code': 'error'}


@app.post('/user')
async def create_user(user: schemas.User, background_tasks: BackgroundTasks):
    background_tasks.add_task(task_user_create, user)
    return {'status': 'success'}


@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    token = create_access_token({'sub': user.dict().get('username')})
    return {'access_token': token, 'token_type': 'bearer'}
