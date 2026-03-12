from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from . import models, storage

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/todos", response_model=List[models.Todo])
def get_todos():
    """
    Returns the full list of todos as a JSON array.
    """
    return storage.get_all_todos()

@app.post("/api/todos", response_model=models.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo_create: models.TodoCreate):
    """
    Accepts a JSON body `{"title": "..."}`, creates a new todo item,
    and returns the created todo.
    """
    created_todo = storage.add_todo(title=todo_create.title)
    return created_todo

@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    """
    Deletes a todo item by its ID. Returns `{"deleted": true}` on success,
    or a 404 error if the todo is not found.
    """
    deleted_todo = storage.delete_todo(todo_id)
    if deleted_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return {"deleted": True}
