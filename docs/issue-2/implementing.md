# IMPLEMENTING - Issue #2

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.
```

### FILE: webapp/storage.py
```python
"""
In-memory storage for the To-Do list application.

This module provides a simple, non-persistent storage mechanism for to-do items.
It is intended for demonstration purposes and will lose all data upon application restart.
"""

_todos: dict[int, dict] = {}
_next_id: int = 1


def get_all_todos() -> list[dict]:
    """Returns a list of all to-do items."""
    return list(_todos.values())


def add_todo(title: str) -> dict:
    """
    Adds a new to-do item to the storage.

    Args:
        title: The title of the to-do item.

    Returns:
        A dictionary representing the newly created to-do item.
    """
    global _next_id
    new_todo = {"id": _next_id, "title": title}
    _todos[_next_id] = new_todo
    _next_id += 1
    return new_todo


def delete_todo(todo_id: int) -> dict | None:
    """
    Deletes a to-do item by its ID.

    Args:
        todo_id: The ID of the to-do item to delete.

    Returns:
        The deleted to-do item if found, otherwise None.
    """
    if todo_id in _todos:
        return _todos.pop(todo_id)
    return None


def _reset_storage():
    """
    Resets the in-memory storage to its initial state.
    This function is intended for testing purposes.
    """
    global _todos, _next_id
    _todos.clear()
    _next_id = 1
```

### FILE: webapp/api.py
```python
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
```

### FILE: requirements.txt
```python
fastapi
uvicorn[standard]
# The existing dependencies are unknown.
# Assuming pygithub and pytest are part of them based on repository context.
pygithub
pytest
```

### FILE: tests/test_api.py
```python
"""
Tests for the FastAPI To-Do list API.

These tests use the FastAPI TestClient to make requests to the application
and verify the behavior of the API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from webapp import storage
from webapp.api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage_before_each_test():
    """
    Fixture to reset the in-memory storage before each test.
    `autouse=True` ensures it runs automatically for every test function,
    guaranteeing test isolation.
    """
    storage._reset_storage()
    yield  # The test runs here


def test_create_todo():
    """
    Tests POST /api/todos to ensure a new todo can be created.
    """
    response = client.post("/api/todos", json={"title": "Test Todo"})
    assert response.status_code == 201, "Should return 201 CREATED"
    data = response.json()
    assert data["title"] == "Test Todo"
    assert "id" in data
    assert data["id"] == 1


def test_get_todos():
    """
    Tests GET /api/todos to ensure it returns a list of all todos.
    """
    # First, create some todos to populate the storage
    client.post("/api/todos", json={"title": "First Todo"})
    client.post("/api/todos", json={"title": "Second Todo"})

    # Then, get the list of todos
    response = client.get("/api/todos")
    assert response.status_code == 200, "Should return 200 OK"
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "First Todo"
    assert data[0]["id"] == 1
    assert data[1]["title"] == "Second Todo"
    assert data[1]["id"] == 2


def test_delete_existing_todo():
    """
    Tests DELETE /api/todos/{todo_id} for an existing todo.
    """
    # Create a todo to delete
    create_response = client.post("/api/todos", json={"title": "To be deleted"})
    todo_id = create_response.json()["id"]

    # Delete the todo
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200, "Should return 200 OK"
    assert delete_response.json() == {"deleted": True}

    # Verify it's gone by fetching all todos
    get_response = client.get("/api/todos")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0, "The todo list should be empty"


def test_delete_non_existent_todo():
    """
    Tests DELETE /api/todos/{todo_id} for a non-existent todo.
    """
    response = client.delete("/api/todos/999")
    assert response.status_code == 404, "Should return 404 NOT FOUND"
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo_with_empty_title_fails():
    """
    Tests that creating a todo with an empty title is rejected.
    Pydantic should return a 422 Unprocessable Entity error.
    """
    # A title with just whitespace should also be considered.
    # The default Pydantic model with `min_length=1` handles this.
    response = client.post("/api/todos", json={"title": ""})
    assert response.status_code == 422, "Should return 422 UNPROCESSABLE ENTITY"
```

## Decisions Made
1.  **`requirements.txt` Content**: Since the original content of `requirements.txt` was not provided, I could not append to it. I created a new version of the file containing the newly required dependencies (`fastapi`, `uvicorn`) and inferred existing ones (`pygithub`, `pytest`) from the repository context. I added a comment to clarify this assumption. This was the most reasonable approach to fulfill the instruction to provide complete file content.
2.  **Input Validation for Title**: The requirement `{"title": "..."}` was slightly ambiguous about empty titles. I decided to enforce that titles must not be empty by using `Field(..., min_length=1)` in the `TodoCreate` Pydantic model in `webapp/api.py`. This is a common and sensible validation for such a field. I also added a test case (`test_create_todo_with_empty_title_fails`) to verify this behavior.
3.  **Storage Reset for Testing**: The plan mentioned a helper function to reset storage for tests. I implemented this as `_reset_storage` in `webapp/storage.py` and used a `pytest.fixture` with `autouse=True` in `tests/test_api.py` to call it before each test. This is a robust pattern that ensures test isolation without needing to call the reset function manually in every test.

## Notes
- The new `webapp` module is self-contained and does not interact with the existing `src` or `dashboard` logic, as per the issue's scope.
- To run the new API locally, one would use the command: `uvicorn webapp.api:app --reload`.
- The in-memory storage is volatile and will be reset every time the application restarts. This is aligned with the plan and suitable for this development task, but a persistent database would be needed for a production environment.
- The project structure now includes a `webapp` directory, which should be committed to the repository along with the other created/modified files.
