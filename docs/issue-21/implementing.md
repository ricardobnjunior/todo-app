# IMPLEMENTING - Issue #21

### FILE: webapp/__init__.py
```python
# This file marks the 'webapp' directory as a Python package.
```

### FILE: webapp/storage.py
```python
"""
In-memory storage for ToDo items.
This is a simple implementation for demonstration purposes and is not thread-safe.
"""

_TODOS = {}
_NEXT_ID = 1


def reset_storage():
    """Resets the in-memory storage to its initial empty state."""
    global _TODOS, _NEXT_ID
    _TODOS = {}
    _NEXT_ID = 1


def get_all_todos() -> list[dict]:
    """Returns a list of all ToDo items."""
    return list(_TODOS.values())


def add_todo(title: str) -> dict:
    """
    Adds a new ToDo item to the storage.

    Args:
        title: The title of the ToDo item.

    Returns:
        The newly created ToDo item as a dictionary.
    """
    global _NEXT_ID
    todo_id = _NEXT_ID
    _TODOS[todo_id] = {"id": todo_id, "title": title}
    _NEXT_ID += 1
    return _TODOS[todo_id]


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a ToDo item by its ID.

    Args:
        todo_id: The ID of the ToDo item to delete.

    Returns:
        True if the item was found and deleted, False otherwise.
    """
    if todo_id in _TODOS:
        del _TODOS[todo_id]
        return True
    return False
```

### FILE: webapp/api.py
```python
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
```

### FILE: requirements.txt
```python
# Agent dependencies
openai
python-dotenv
apprise
PyGithub
python-json-logger
tiktoken

# Dashboard dependencies
streamlit
pandas
plotly
requests

# WebApp dependencies
fastapi
uvicorn[standard]
httpx
```

### FILE: tests/test_api.py
```python
"""
Tests for the FastAPI ToDo list API.
"""

import pytest
from fastapi.testclient import TestClient

from webapp.api import app
from webapp import storage


@pytest.fixture(autouse=True)
def clean_storage_before_tests():
    """Fixture to ensure storage is reset before each test."""
    storage.reset_storage()


client = TestClient(app)


def test_create_and_get_todo():
    """
    Test creating a new todo via POST and then retrieving it via GET.
    """
    # 1. POST a new todo
    response_post = client.post(
        "/api/todos",
        json={"title": "First Todo"},
    )
    assert response_post.status_code == 201
    created_todo = response_post.json()
    assert "id" in created_todo
    assert created_todo["id"] == 1
    assert created_todo["title"] == "First Todo"

    # 2. GET all todos and verify the new one is there
    response_get = client.get("/api/todos")
    assert response_get.status_code == 200
    todos_list = response_get.json()
    assert len(todos_list) == 1
    assert todos_list[0]["id"] == created_todo["id"]
    assert todos_list[0]["title"] == created_todo["title"]


def test_delete_existing_todo():
    """
    Test deleting an existing todo.
    """
    # 1. Create a todo to delete
    response_post = client.post(
        "/api/todos",
        json={"title": "Todo to be deleted"},
    )
    assert response_post.status_code == 201
    todo_id = response_post.json()["id"]

    # 2. Delete the todo
    response_delete = client.delete(f"/api/todos/{todo_id}")
    assert response_delete.status_code == 200
    assert response_delete.json() == {"deleted": True}

    # 3. Verify it's gone
    response_get = client.get("/api/todos")
    assert response_get.status_code == 200
    assert response_get.json() == []


def test_delete_non_existent_todo():
    """
    Test that deleting a non-existent todo returns a 404 error.
    """
    # Attempt to delete a todo with an ID that doesn't exist
    response_delete = client.delete("/api/todos/999")
    assert response_delete.status_code == 404
    assert response_delete.json() == {"detail": "Todo not found"}
```

## Decisions Made
1.  **`webapp/storage.py` Design**: I chose a simple dictionary and an integer counter for the in-memory store. A `reset_storage()` function was added specifically for test isolation, which is a common and practical pattern for this type of setup.
2.  **`requirements.txt` Modification**: I appended the new dependencies (`fastapi`, `uvicorn[standard]`, `httpx`) under a new comment section `# WebApp dependencies` to keep the file organized and easy to understand.
3.  **Test Structure in `tests/test_api.py`**:
    *   I used a pytest fixture with `autouse=True` to automatically reset the storage before each test function. This is cleaner than manually calling `storage.reset_storage()` in every test and ensures test isolation.
    *   For testing the create-read flow, I combined the `POST` and `GET` assertions into a single test function `test_create_and_get_todo`. This creates a clear, scenario-based test that is easy to follow.
    *   The test for deletion also verifies the state change by making a `GET` call after the `DELETE` to ensure the list is empty, making the test more robust.
4.  **CORS Configuration**: As requested, I configured the `CORSMiddleware` to be wide open (`allow_origins=["*"]`, etc.). This is suitable for development but I noted in the research that it's not secure for production.
5.  **Pydantic Models**: I created two distinct Pydantic models, `TodoIn` and `TodoOut`, to separate the request payload structure from the response structure, which is a FastAPI best practice. `TodoIn` only requires a `title`, whereas `TodoOut` includes the server-generated `id`.

## Notes
- The implementation is now complete and fulfills all requirements from the issue description.
- The new `webapp` is a self-contained application, completely separate from the existing `src` and `dashboard` codebases.
- The tests in `tests/test_api.py` are comprehensive for the specified CRUD operations.
- To run the application locally, one would use a command like `uvicorn webapp.api:app --reload` from the project root. The API would then be available at `http://127.0.0.1:8000`.
- The in-memory storage is not persistent and will be reset every time the application restarts. This is expected given the scope of the issue.
