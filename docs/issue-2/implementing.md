# IMPLEMENTING - Issue #2

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.

```

### FILE: webapp/models.py
```python
from pydantic import BaseModel

class TodoCreate(BaseModel):
    """Model for creating a new todo item."""
    title: str

class Todo(BaseModel):
    """Model representing a todo item."""
    id: int
    title: str

```

### FILE: webapp/storage.py
```python
from typing import Optional, Dict, List

# In-memory data store for todos
_todos: Dict[int, Dict] = {}
_next_id = 1

def reset_storage():
    """Resets the in-memory storage. Used for testing."""
    global _todos, _next_id
    _todos = {}
    _next_id = 1

def get_all_todos() -> List[Dict]:
    """Returns a list of all todo items."""
    return list(_todos.values())

def add_todo(title: str) -> Dict:
    """Adds a new todo item to the store."""
    global _next_id
    new_todo = {
        "id": _next_id,
        "title": title
    }
    _todos[_next_id] = new_todo
    _next_id += 1
    return new_todo

def delete_todo(todo_id: int) -> Optional[Dict]:
    """Deletes a todo item by its ID."""
    if todo_id in _todos:
        return _todos.pop(todo_id)
    return None

```

### FILE: webapp/api.py
```python
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

```

### FILE: tests/test_api.py
```python
import pytest
from fastapi.testclient import TestClient

from webapp.api import app
from webapp import storage

# This fixture will be automatically used by all tests in this file
@pytest.fixture(autouse=True)
def reset_storage_before_each_test():
    """
    Resets the in-memory storage before each test function runs to ensure
    test isolation.
    """
    storage.reset_storage()

client = TestClient(app)

def test_create_and_get_todos():
    """
    Tests creating a new todo via POST and then retrieving the list via GET.
    """
    # 1. Initially, the list of todos should be empty
    initial_response = client.get("/api/todos")
    assert initial_response.status_code == 200
    assert initial_response.json() == []

    # 2. POST a new todo
    response = client.post("/api/todos", json={"title": "Test my new API"})
    assert response.status_code == 201, "Expected 201 Created for a new resource"
    
    created_todo = response.json()
    assert "id" in created_todo
    assert created_todo["id"] == 1
    assert created_todo["title"] == "Test my new API"

    # 3. GET all todos to verify the created todo is in the list
    get_response = client.get("/api/todos")
    assert get_response.status_code == 200
    
    todos_list = get_response.json()
    assert isinstance(todos_list, list)
    assert len(todos_list) == 1
    assert todos_list[0] == created_todo

def test_delete_todo():
    """
    Tests deleting an existing todo.
    """
    # 1. Create a todo to be deleted
    create_response = client.post("/api/todos", json={"title": "This will be deleted"})
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    # 2. Delete the todo
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"deleted": True}

    # 3. Verify the todo is gone by fetching the list again
    get_response = client.get("/api/todos")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0

def test_delete_nonexistent_todo():
    """
    Tests that attempting to delete a non-existent todo returns a 404 error.
    """
    response = client.delete("/api/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

```

### FILE: requirements.txt
```
openai
PyGithub
python-dotenv
pytest
httpx
fastapi
uvicorn[standard]

```

## Decisions Made
1.  **`requirements.txt` Content**: The original content of `requirements.txt` was not provided. To fulfill the instruction of outputting a complete file, I inferred some likely existing dependencies (`openai`, `PyGithub`, `python-dotenv`, `pytest`) from the repository context and added them to `requirements.txt` along with the new required dependencies (`fastapi`, `uvicorn[standard]`, `httpx`). This is a safer approach than overwriting the file with only the new dependencies.
2.  **`httpx` Dependency**: The PLAN did not explicitly mention `httpx` as a dependency. However, FastAPI's `TestClient` requires `httpx` to function. To ensure the created tests in `tests/test_api.py` are runnable, I added `httpx` to `requirements.txt`.
3.  **In-Memory Storage Reset**: To ensure test isolation, I created a `reset_storage()` function in the `webapp.storage` module. This function is called before each test using a `pytest` fixture with `autouse=True` in `tests/test_api.py`.
4.  **CORS Middleware**: As requested, CORS middleware was added to the FastAPI application to allow all origins, methods, and headers (`*`). This is a permissive setting suitable for development but might need to be tightened for production environments.

## Notes
- The new ToDo list functionality is self-contained within the `webapp` directory.
- To run the new API server locally, you can use the command: `uvicorn webapp.api:app --reload`.
- The tests for the new API are located in `tests/test_api.py` and can be run with `pytest`. They use FastAPI's `TestClient` and do not require a live server.
- The `requirements.txt` file has been updated. Please ensure you install the new dependencies by running: `pip install -r requirements.txt`.
