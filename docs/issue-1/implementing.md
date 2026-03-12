# IMPLEMENTING - Issue #1

### FILE: webapp/__init__.py
```python
# This file marks the 'webapp' directory as a Python package.
```

### FILE: webapp/models.py
```python
from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Todo(BaseModel):
    """
    Pydantic model representing a single ToDo task.
    """
    id: int
    title: str
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

```

### FILE: webapp/storage.py
```python
from __future__ import annotations

from .models import Todo

# In-memory storage for todos
todos: list[dict] = []

# Counter for generating unique todo IDs
_next_id: int = 1


def add_todo(title: str) -> dict:
    """
    Creates a new todo with an auto-incremented ID and a timestamp,
    adds it to the in-memory list, and returns it.

    Args:
        title: The title of the todo task.

    Returns:
        A dictionary representing the newly created todo.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    _next_id += 1

    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    return todo_dict


def list_todos() -> list[dict]:
    """
    Returns a copy of the list of all todos.

    Returns:
        A list of dictionaries, where each dictionary represents a todo.
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
    original_len = len(todos)
    # Rebuild the list in place, excluding the todo with the matching id
    todos[:] = [t for t in todos if t['id'] != todo_id]
    return len(todos) < original_len

```

### FILE: tests/test_storage.py
```python
from __future__ import annotations

import pytest
from datetime import datetime
from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage():
    """Reset the in-memory storage before each test."""
    storage.todos.clear()
    storage._next_id = 1


def test_add_todo():
    """
    Tests that add_todo creates a todo with the correct structure and adds it to storage.
    """
    title = "My first todo"
    new_todo = storage.add_todo(title)

    # Check returned structure
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo

    # Check if created_at is a valid ISO 8601 string
    try:
        # Pydantic's default factory produces a string compatible with fromisoformat
        datetime.fromisoformat(new_todo["created_at"])
    except (ValueError, TypeError):
        pytest.fail(f"created_at '{new_todo['created_at']}' is not a valid ISO 8601 string")

    # Check if it was added to storage
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos():
    """
    Tests that list_todos returns all added items.
    """
    assert storage.list_todos() == []

    todo1 = storage.add_todo("First")
    todo2 = storage.add_todo("Second")

    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos


def test_delete_existing_todo():
    """
    Tests that delete_todo removes an existing item and returns True.
    """
    todo_to_delete = storage.add_todo("To be deleted")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(todo_to_delete["id"])

    assert result is True
    assert len(storage.list_todos()) == 0


def test_delete_non_existent_todo():
    """
    Tests that delete_todo returns False when the item does not exist.
    """
    storage.add_todo("Should not be deleted")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(999)  # Non-existent ID

    assert result is False
    assert len(storage.list_todos()) == 1


def test_id_auto_increment_after_deletion():
    """
    Tests that the ID counter increments correctly and does not reuse IDs after deletion.
    """
    todo1 = storage.add_todo("Item 1")
    todo2 = storage.add_todo("Item 2")
    todo3 = storage.add_todo("Item 3")

    # IDs should be 1, 2, 3
    assert todo1["id"] == 1
    assert todo2["id"] == 2
    assert todo3["id"] == 3

    # Delete the middle one
    deleted = storage.delete_todo(2)
    assert deleted is True

    # Add a new one
    todo4 = storage.add_todo("Item 4")

    # New ID should be 4, not 2
    assert todo4["id"] == 4

    # Check the final list of IDs
    current_todos = storage.list_todos()
    current_ids = [t["id"] for t in current_todos]
    assert current_ids == [1, 3, 4]

```

### FILE: requirements.txt
```python
fastapi
uvicorn
ghapi
humanize
openai
streamlit
python-dotenv
requests
loguru
pydantic
```

## Decisions Made
1.  **Directory Structure**: The new feature is placed in a new top-level `webapp` directory. This isolates it from the existing `src` codebase, which appears to be for a different purpose (agent orchestration).
2.  **Timestamp Format**: For the `created_at` field, I chose `datetime.now(timezone.utc).isoformat()`. This provides a timezone-aware ISO 8601 string, which is more robust than a naive datetime, and is a modern best practice.
3.  **Pydantic Versioning**: I used `.model_dump()` to convert the Pydantic model to a dictionary. This is the standard method in Pydantic v2 and is recommended over the deprecated `.dict()` from v1.
4.  **Test State Isolation**: I implemented a `pytest` fixture with `autouse=True` to reset the in-memory storage state before each test. This is crucial for ensuring tests are independent and reliable.
5.  **`requirements.txt` Modification**: I added `pydantic` to the existing `requirements.txt` file. I maintained the existing list of packages and simply appended the new one, as the exact order or grouping was not specified.

## Notes
-   The in-memory storage solution in `webapp/storage.py` is simple and sufficient for the requirements but is not thread-safe. If this were to be used in a concurrent environment (e.g., a multi-threaded web server), access to the global `todos` list and `_next_id` counter would need to be protected by a lock (e.g., `threading.Lock`) to prevent race conditions.
-   The implementation follows the plan exactly, creating the model, storage layer, and a comprehensive suite of tests covering all specified requirements.
-   `from __future__ import annotations` has been added to the new Python files for better forward-compatibility with type hints, even though it might not be strictly necessary if the project's minimum Python version is 3.9+.
