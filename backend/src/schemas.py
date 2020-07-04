from pydantic import BaseModel


class TodoPost(BaseModel):
    title: str
    completed: bool


class Todo(TodoPost):
    id: int
