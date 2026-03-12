from pydantic import BaseModel

class TodoCreate(BaseModel):
    """Model for creating a new todo item."""
    title: str

class Todo(BaseModel):
    """Model representing a todo item."""
    id: int
    title: str
