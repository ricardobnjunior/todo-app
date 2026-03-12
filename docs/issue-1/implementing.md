# IMPLEMENTING - Issue #1

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.

```

### FILE: webapp/models.py
```python
"""
Data models for the ToDo application.
"""
from pydantic import BaseModel, Field
from datetime import datetime, timezone


def _generate_iso_timestamp() -> str:
    """Returns the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class Todo(BaseModel):
    """
    Represents a single ToDo task.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=_generate_iso_timestamp)

```

### FILE: webapp/storage.py
```python
"""
In-memory storage for ToDo items.

This module provides a simple, non-persistent storage layer for ToDo tasks.
The data is stored in a module-level list.
"""
from datetime import datetime, timezone
from typing import List, Dict, Any

# In-memory database for todos
todos: List[Dict[str, Any]] = []

# Counter for generating unique todo IDs
_next_id: int = 1


def add_todo(title: str) -> Dict[str, Any]:
    """
    Creates a new todo, adds it to the in-memory list, and returns it.

    Args:
        title: The title of the todo task.

    Returns:
        A dictionary representing the newly created todo.
    """
    global _next_id
    new_todo = {
        "id": _next_id,
        "title": title,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    todos.append(new_todo)
    _next_id += 1
    return new_todo


def list_todos() -> List[Dict[str, Any]]:
    """
    Returns the complete list of todos.

    Returns:
        A copy of the list of all todo items.
    """
    return todos.copy()


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a todo by its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was found and deleted, False otherwise.
    """
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo.get("id") != todo_id]
    return len(todos) < initial_length

```

### FILE: tests/test_storage.py
```python
"""
Tests for the in-memory storage module.
"""
import pytest
from datetime import datetime, timezone, timedelta

from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage_state():
    """
    A fixture that automatically runs before each test to reset the storage.
    This ensures that tests are isolated and don't interfere with each other.
    """
    storage.todos.clear()
    # Resetting a non-public variable is generally discouraged, but necessary
    # for testing this specific implementation.
    storage._next_id = 1
    yield


def test_add_todo():
    """
    Tests that add_todo correctly creates a task, returns it, and stores it.
    """
    title = "My first task"
    new_todo = storage.add_todo(title=title)

    # 1. Check the returned dictionary
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo

    # Check if a valid ISO timestamp was created
    created_at_dt = datetime.fromisoformat(new_todo["created_at"])
    assert created_at_dt.tzinfo is not None
    # Check if the timestamp is recent (within the last 5 seconds)
    assert datetime.now(timezone.utc) - created_at_dt < timedelta(seconds=5)

    # 2. Check the side effect (storage)
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos():
    """
    Tests that list_todos returns all added items.
    """
    assert storage.list_todos() == []  # Should be empty initially

    storage.add_todo("Task 1")
    storage.add_todo("Task 2")
    storage.add_todo("Task 3")

    all_todos = storage.list_todos()
    assert len(all_todos) == 3
    assert all_todos[0]["id"] == 1
    assert all_todos[1]["title"] == "Task 2"
    assert all_todos[2]["id"] == 3


def test_delete_existing_todo():
    """
    Tests that delete_todo with an existing ID returns True and removes the item.
    """
    todo = storage.add_todo("Task to be deleted")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(todo["id"])
    assert result is True
    assert len(storage.list_todos()) == 0


def test_delete_non_existent_todo():
    """
    Tests that delete_todo with a non-existent ID returns False.
    """
    storage.add_todo("An existing task")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(999)  # A non-existent ID
    assert result is False
    assert len(storage.list_todos()) == 1


def test_id_auto_increment_after_deletion():
    """
    Tests that IDs auto-increment correctly even after an item is deleted.
    IDs should be 1, 3, 4 after adding 3, deleting the middle one, and adding one more.
    """
    # Add three todos
    t1 = storage.add_todo("Task 1")
    t2 = storage.add_todo("Task 2")
    t3 = storage.add_todo("Task 3")
    assert [t["id"] for t in storage.list_todos()] == [1, 2, 3]

    # Delete the middle one
    deleted = storage.delete_todo(t2["id"])
    assert deleted is True
    assert [t["id"] for t in storage.list_todos()] == [1, 3]

    # Add another one
    t4 = storage.add_todo("Task 4")
    assert t4["id"] == 4, "The next ID should be 4, not re-using 2"

    # Check final state of IDs
    final_ids = [t["id"] for t in storage.list_todos()]
    assert final_ids == [1, 3, 4]

```

### FILE: requirements.txt
```python
fastapi
ghapi
openai
pydantic
python-dotenv
pyyaml
rich
uvicorn
```

## Decisions Made
1.  **Pydantic Model Separation**: The issue requested a Pydantic `Todo` model but also that the `storage.py` functions work with and return `dict` types. I honored this by defining the `Todo` model in `webapp/models.py` as the canonical schema, but kept the implementations in `webapp/storage.py` using plain dictionaries. This keeps the storage layer simple and without a direct dependency on Pydantic for its runtime logic.
2.  **Timestamp Generation**: The `webapp/models.py` `Todo` model uses `Field(default_factory=...)` to generate the `created_at` timestamp, which is the idiomatic Pydantic way. In `webapp/storage.py`, I manually generated the timestamp using `datetime.now(timezone.utc).isoformat()` inside the `add_todo` function to keep it self-contained and align with the `dict`-based approach. I ensured both methods produce timezone-aware ISO 8601 strings.
3.  **Test State Reset**: To handle the module-level state in `storage.py`, I used a `pytest` fixture with `autouse=True` in `tests/test_storage.py`. This fixture resets the `todos` list and `_next_id` counter before each test, guaranteeing test isolation and preventing flaky tests. The fixture directly modifies the non-public `_next_id` variable, which is acceptable in a test context to properly reset state.
4.  **`delete_todo` Implementation**: I chose a list comprehension (`todos = [t for t in todos if ...]`) for the `delete_todo` function. This is a robust and readable way to create a new list without the item to be removed, which also handles the case where the item doesn't exist gracefully.
5.  **`requirements.txt` update**: I added `pydantic` to the `requirements.txt` file and kept the existing dependencies. I sorted the list alphabetically for better maintenance.

## Notes
- The created `webapp` directory and its contents are self-contained. This can serve as the foundation for a future web API (e.g., using FastAPI) that would import the model from `models.py` and the storage functions from `storage.py`.
- The `storage.py` module is intentionally simple and not thread-safe. For a real-world application, concurrency control (e.g., `threading.Lock`) would be necessary if the application were multi-threaded.
- The tests cover all functional requirements specified in the issue description and follow the patterns established in the project's existing test suite.
