# IMPLEMENTING - Issue #1

### FILE: requirements.txt
```
ghapi
openai
pydantic
python-dotenv
rich
```

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.
```

### FILE: webapp/models.py
```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Todo(BaseModel):
    """
    Pydantic model for a ToDo item.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
```

### FILE: webapp/storage.py
```python
from .models import Todo

# In-memory storage components
todos: list[dict] = []
_next_id: int = 1


def add_todo(title: str) -> dict:
    """
    Creates a new todo with an auto-incremented ID and current timestamp,
    adds it to the in-memory list, and returns the created todo as a dictionary.

    Args:
        title: The title of the todo.

    Returns:
        A dictionary representing the new todo.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    _next_id += 1
    return todo_dict


def list_todos() -> list[dict]:
    """
    Returns a copy of the list of all todo items.

    Returns:
        A list of dictionaries, where each dictionary is a todo.
    """
    return todos.copy()


def delete_todo(todo_id: int) -> bool:
    """
    Removes a todo from the list based on its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was found and removed, False otherwise.
    """
    initial_count = len(todos)
    # Rebuild the list, excluding the todo with the matching ID.
    # Modifying the list in-place to avoid 'global' keyword.
    todos[:] = [todo for todo in todos if todo.get("id") != todo_id]
    return len(todos) < initial_count
```

### FILE: tests/test_storage.py
```python
import re
from datetime import datetime, timezone

import pytest

from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage():
    """
    This fixture automatically runs before each test to ensure a clean state.
    It clears the list of todos and resets the ID counter.
    """
    storage.todos.clear()
    storage._next_id = 1


def test_add_todo():
    """
    Tests that adding a todo returns a correctly structured dictionary
    and successfully adds it to the storage list.
    """
    title = "Buy groceries"
    new_todo = storage.add_todo(title)

    # 1. Verify the structure and content of the returned dictionary
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo

    # 2. Verify the timestamp is a valid ISO 8601 string and is recent
    try:
        created_time = datetime.fromisoformat(new_todo["created_at"])
        assert created_time.tzinfo is not None
        time_difference = datetime.now(timezone.utc) - created_time
        assert time_difference.total_seconds() < 2
    except (ValueError, TypeError):
        pytest.fail("created_at is not a valid ISO 8601 timestamp string.")

    # 3. Verify the internal state of the storage module
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo
    assert storage._next_id == 2


def test_list_todos():
    """
    Tests that listing todos returns all items that have been added.
    """
    # Initially, the list should be empty
    assert storage.list_todos() == []

    # Add items and verify they are listed correctly
    todo1 = storage.add_todo("First task")
    todo2 = storage.add_todo("Second task")

    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos


def test_delete_existing_todo():
    """
    Tests that deleting an existing todo returns True and removes the
    item from the list.
    """
    todo1 = storage.add_todo("Task to be deleted")
    todo2 = storage.add_todo("Task to keep")

    result = storage.delete_todo(todo1["id"])

    # Verify the function returned True
    assert result is True

    # Verify the item was removed from storage
    remaining_todos = storage.list_todos()
    assert len(remaining_todos) == 1
    assert remaining_todos[0] == todo2


def test_delete_non_existent_todo():
    """
    Tests that attempting to delete a non-existent todo returns False
    and does not alter the storage list.
    """
    storage.add_todo("A single task")

    result = storage.delete_todo(999)  # A non-existent ID

    # Verify the function returned False
    assert result is False

    # Verify the storage list is unchanged
    all_todos = storage.list_todos()
    assert len(all_todos) == 1


def test_ids_auto_increment_correctly():
    """
    Tests that IDs are unique and increment correctly, even after
    items have been deleted from the middle of the list.
    """
    # Add three items, IDs should be 1, 2, 3
    t1 = storage.add_todo("Task 1")
    t2 = storage.add_todo("Task 2")
    t3 = storage.add_todo("Task 3")

    assert t1["id"] == 1
    assert t2["id"] == 2
    assert t3["id"] == 3
    assert storage._next_id == 4

    # Delete the middle item
    was_deleted = storage.delete_todo(2)
    assert was_deleted is True

    # Add a new item
    t4 = storage.add_todo("Task 4")

    # The new ID should continue from the counter (4), not fill the gap (2)
    assert t4["id"] == 4
    assert storage._next_id == 5

    # Check the final state of IDs in the list
    final_todos = storage.list_todos()
    final_ids = [t["id"] for t in final_todos]
    assert sorted(final_ids) == [1, 3, 4]
```

## Decisions Made
1.  **`requirements.txt` Content**: The original content of `requirements.txt` was not provided. Based on imports found in other project files (`ghapi`, `openai`, `rich`, `python-dotenv`), I created a plausible `requirements.txt` and added `pydantic` to it, keeping the list alphabetized for consistency.
2.  **Pydantic Version**: I assumed the use of Pydantic v2+ and used `.model_dump()` for converting a model instance to a dictionary, as this is the current standard.
3.  **Timestamp Format**: For the `created_at` field, I used `datetime.now(timezone.utc).isoformat()`. This produces a timezone-aware ISO 8601 string, which is robust and unambiguous.
4.  **`delete_todo` Implementation**: I chose to implement `delete_todo` by rebuilding the list using a list comprehension (`todos[:] = [...]`). This modifies the list in-place, which is efficient and avoids needing to declare `todos` as `global`. It's also safer than trying to remove items while iterating.
5.  **Test State Reset**: For test isolation in `tests/test_storage.py`, I used a `pytest` fixture with `autouse=True` to directly modify the state of the `storage` module (`storage.todos.clear()` and `storage._next_id = 1`). This is simple, effective, and sufficient for this use case.
6.  **Directory Creation**: The request implies creating a new `webapp/` directory. My output format produces files with their full paths, which implicitly defines this new directory structure.

## Notes
- The created in-memory storage in `webapp/storage.py` is not thread-safe. If this were to be used in a multi-threaded server context, access to `todos` and `_next_id` (specifically in `add_todo` and `delete_todo`) would need to be protected by a lock (e.g., `threading.Lock`). For the current scope, this is not an issue.
- The `created_at` timestamp check in `tests/test_storage.py` is robust, verifying not only that the string can be parsed as a valid ISO timestamp but also that it's recent (within 2 seconds of the test execution time), confirming it was generated on-the-fly.
- The tests fully cover the requirements outlined in the issue description, including the specific scenario for ID auto-incrementation.
