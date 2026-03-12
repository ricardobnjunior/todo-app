"""
FastAPI application for the To-Do list REST API.

This module defines the API endpoints for CRUD (Create, Read, Delete) operations
on to-do items.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from webapp import storage

app = FastAPI()

# Add CORS middleware to allow cross-origin requests from any domain.
# This is necessary for the frontend (index.html) to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for data validation and serialization.

class TodoCreate(BaseModel):
    """Request model for creating a new to-do item."""
    title: str = Field(..., min_length=1, description="Title of the to-do item.")


class Todo(BaseModel):
    """Response model for a to-do item."""
    id: int
    title: str


# API Endpoints

@app.get("/api/todos", response_model=list[Todo])
def get_todos():
    """Retrieve all to-do items."""
    return storage.get_all_todos()


@app.post("/api/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """Create a new to-do item."""
    created_todo = storage.add_todo(title=todo.title)
    return created_todo


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a to-do item by its ID."""
    deleted_todo = storage.delete_todo(todo_id)
    if deleted_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return {"deleted": True}
