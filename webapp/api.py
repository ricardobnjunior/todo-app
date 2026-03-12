"""
FastAPI application for the ToDo list API.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from webapp import storage

app = FastAPI(
    title="ToDo List API",
    description="A simple API for managing a ToDo list.",
    version="1.0.0",
)

# CORS Middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Pydantic models for data validation and serialization
class TodoIn(BaseModel):
    """Request model for creating a ToDo."""
    title: str


class TodoOut(BaseModel):
    """Response model for a ToDo item."""
    id: int
    title: str


@app.get(
    "/api/todos",
    response_model=List[TodoOut],
    summary="Get all ToDo items",
    tags=["Todos"],
)
def get_todos():
    """
    Retrieve a list of all ToDo items.
    """
    return storage.get_all_todos()


@app.post(
    "/api/todos",
    response_model=TodoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new ToDo item",
    tags=["Todos"],
)
def create_todo(todo: TodoIn):
    """
    Create a new ToDo item.
    The new item is returned with its assigned ID.
    """
    created_todo = storage.add_todo(title=todo.title)
    return created_todo


@app.delete(
    "/api/todos/{todo_id}",
    summary="Delete a ToDo item",
    tags=["Todos"],
)
def delete_todo(todo_id: int):
    """
    Delete a ToDo item by its ID.
    Returns a confirmation if successful, otherwise a 404 error.
    """
    was_deleted = storage.delete_todo(todo_id=todo_id)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return {"deleted": True}
