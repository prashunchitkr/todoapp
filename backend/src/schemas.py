from pydantic import BaseModel


class TodoPost(BaseModel):
    title: str
    completed: bool = False


class Todo(TodoPost):
    id: int
