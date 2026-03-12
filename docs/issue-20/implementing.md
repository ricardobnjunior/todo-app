# IMPLEMENTING - Issue #20

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.

```

### FILE: requirements.txt
```python
# Main application dependencies
ghapi
python-dotenv
openai
rich

# Dashboard dependencies
streamlit
pandas
plotly

# Webapp dependencies
pydantic
```

### FILE: webapp/models.py
```python
"""
Pydantic data models for the webapp.
"""
from datetime import datetime, timezone
from pydantic import BaseModel, Field


def get_current_time_iso() -> str:
    """Returns the current time in UTC ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class Todo(BaseModel):
    """
    Represents a single To-Do item.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=get_current_time_iso)

```

### FILE: webapp/storage.py
```python
"""
In-memory storage for To-Do items.

This module provides a simple in-memory database for managing To-Do items.
The data is stored in a module-level list and will be reset when the
application restarts.
"""

from typing import List, Dict

from webapp.models import Todo

# In-memory database of To-Do items
todos: List[Dict] = []
_next_id: int = 1


def add_todo(title: str) -> Dict:
    """
    Creates a new To-Do item, adds it to the in-memory list, and returns it.

    Args:
        title: The title of the To-Do item.

    Returns:
        A dictionary representing the newly created To-Do item.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    
    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    
    _next_id += 1
    return todo_dict


def list_todos() -> List[Dict]:
    """
    Returns the list of all To-Do items.

    Returns:
        A list of dictionaries, where each dictionary is a To-Do item.
    """
    return todos[:]


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a To-Do item by its ID.

    Args:
        todo_id: The ID of the To-Do item to delete.

    Returns:
        True if the item was found and deleted, False otherwise.
    """
    global todos
    todo_to_delete = None
    for todo in todos:
        if todo["id"] == todo_id:
            todo_to_delete = todo
            break
            
    if todo_to_delete:
        todos.remove(todo_to_delete)
        return True
    
    return False

```

### FILE: tests/test_storage.py
```python
"""
Tests for the in-memory To-Do storage.
"""

import importlib
import pytest
from datetime import datetime, timezone

# Import the module to be tested
from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage():
    """
    Fixture to reset the storage module's state before each test.
    This ensures that tests are isolated from each other.
    """
    importlib.reload(storage)


def test_add_todo():
    """
    Verifies that adding a todo returns the correct structure and persists the item.
    """
    title = "Buy milk"
    
    # 1. Add a new todo
    new_todo = storage.add_todo(title)
    
    # 2. Verify the returned dictionary structure and content
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo
    assert isinstance(new_todo["created_at"], str)
    
    # Verify the timestamp is a valid ISO 8601 format
    try:
        datetime.fromisoformat(new_todo["created_at"].replace('Z', '+00:00'))
    except ValueError:
        pytest.fail("created_at is not a valid ISO 8601 timestamp")

    # 3. Verify the item is in the main list
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos():
    """
    Verifies that listing todos returns all added items.
    """
    # Initially, the list should be empty
    assert storage.list_todos() == []

    # Add two items
    todo1 = storage.add_todo("First task")
    todo2 = storage.add_todo("Second task")

    # List todos and verify
    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert all_todos == [todo1, todo2]


def test_delete_todo_existing():
    """
    Verifies that deleting an existing todo returns True and removes it from the list.
    """
    # 1. Add a todo
    todo = storage.add_todo("Task to be deleted")
    assert len(storage.list_todos()) == 1

    # 2. Delete the todo
    result = storage.delete_todo(todo["id"])

    # 3. Verify the result and the state of the list
    assert result is True
    assert len(storage.list_todos()) == 0


def test_delete_todo_non_existent():
    """
    Verifies that deleting a non-existent todo returns False and doesn't change the list.
    """
    # 1. Add a todo
    storage.add_todo("An existing task")
    assert len(storage.list_todos()) == 1

    # 2. Attempt to delete a non-existent todo
    result = storage.delete_todo(999) # An ID that does not exist

    # 3. Verify the result and the state of the list
    assert result is False
    assert len(storage.list_todos()) == 1


def test_id_auto_increment():
    """
    Verifies that IDs auto-increment correctly, even after deletions.
    IDs should be 1, 2, 3 -> delete 2 -> add new -> new ID is 4.
    """
    # 1. Add three todos and check their IDs
    todo1 = storage.add_todo("Task 1")
    todo2 = storage.add_todo("Task 2")
    todo3 = storage.add_todo("Task 3")
    assert todo1["id"] == 1
    assert todo2["id"] == 2
    assert todo3["id"] == 3

    # 2. Delete the middle one
    delete_result = storage.delete_todo(2)
    assert delete_result is True

    # 3. Check the current list of IDs
    current_ids = [t["id"] for t in storage.list_todos()]
    assert current_ids == [1, 3]

    # 4. Add another todo
    todo4 = storage.add_todo("Task 4")

    # 5. Verify the new ID is 4 (and not 2)
    assert todo4["id"] == 4

    # 6. Verify the final list of IDs
    final_ids = [t["id"] for t in storage.list_todos()]
    assert final_ids == [1, 3, 4]

```

## Decisions Made
1.  **Dependency Management**: I've added `pydantic` to `requirements.txt` under a new comment section `# Webapp dependencies` to keep the file organized, following the existing pattern of separating main and dashboard dependencies.
2.  **Pydantic Version**: I used `model_dump()` which is the standard for Pydantic v2. This is a modern choice for new code.
3.  **Timestamp Generation**: I created a helper function `get_current_time_iso` within `webapp/models.py` and passed it to the `default_factory`. This makes the `Todo` model definition a bit cleaner and the timestamp logic more explicit. I used `datetime.now(timezone.utc)` to ensure timezone-aware and unambiguous timestamps, which is a best practice.
4.  **Test Isolation**: The `reset_storage` fixture in `tests/test_storage.py` uses `importlib.reload(storage)` and is set to `autouse=True`. This is the most reliable way to ensure the in-memory `todos` list and `_next_id` counter are reset to their initial state before every single test function runs, preventing state leakage between tests.
5.  **Return Value of list_todos**: The function `list_todos` returns `todos[:]`, which is a shallow copy of the list. This is a good practice to prevent external code from directly modifying the internal storage list by accident (e.g., by calling `.append()` on the returned list).

## Notes
- The implemented storage layer is in-memory and therefore not persistent. All data will be lost when the application process stops. This is consistent with the issue requirements.
- The storage layer is not thread-safe. In a concurrent environment, race conditions could occur (e.g., when multiple threads call `add_todo` simultaneously). For the scope of this simple ToDo application, this is an acceptable limitation. If concurrency becomes a requirement, locking mechanisms (`threading.Lock`) would need to be introduced around the shared state (`todos` list and `_next_id` counter).
- All created files and tests strictly follow the plan and meet all requirements outlined in the issue.
