# IMPLEMENTING - Issue #1

I will now execute the plan to implement the data layer for the ToDo list application.

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.

```

### FILE: requirements.txt
```python
# Core application dependencies for src/
ghapi
openai

# Webapp dependencies
pydantic

# Testing dependencies
pytest
```

### FILE: webapp/models.py
```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def get_current_time_iso() -> str:
    """Returns the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()

class Todo(BaseModel):
    """
    Pydantic model for a ToDo item.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=get_current_time_iso)

```

### FILE: webapp/storage.py
```python
from webapp.models import Todo

# Module-level in-memory storage for todos
# A list of dictionaries, where each dictionary represents a todo.
todos: list[dict] = []

# Module-level counter for the next available todo ID.
_next_id: int = 1

def add_todo(title: str) -> dict:
    """
    Creates a new todo with a unique ID and timestamp, adds it to the
    in-memory list, and returns the new todo as a dictionary.

    Args:
        title: The title of the todo.

    Returns:
        A dictionary representing the newly created todo.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    _next_id += 1
    return todo_dict

def list_todos() -> list[dict]:
    """
    Returns a copy of the list of all todos.

    Returns:
        A list of dictionaries, where each dictionary is a todo.
    """
    return todos[:]

def delete_todo(todo_id: int) -> bool:
    """
    Deletes a todo from the in-memory list based on its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was found and deleted, False otherwise.
    """
    global todos
    initial_len = len(todos)
    todos = [todo for todo in todos if todo.get("id") != todo_id]
    return len(todos) < initial_len

```

### FILE: tests/test_storage.py
```python
import pytest
from datetime import datetime
from webapp import storage

@pytest.fixture(autouse=True)
def reset_storage():
    """
    This fixture automatically runs before each test.
    It resets the in-memory storage to a clean state, ensuring
    that tests are isolated from each other.
    """
    storage.todos.clear()
    storage._next_id = 1
    # Yield control to the test function
    yield
    # Teardown (optional, but good practice if needed)
    storage.todos.clear()
    storage._next_id = 1

def test_add_todo():
    """
    Tests if add_todo creates a todo with the correct structure and data.
    """
    title = "My first test todo"
    new_todo = storage.add_todo(title)

    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo
    # Verify created_at is a valid ISO 8601 timestamp string
    try:
        datetime.fromisoformat(new_todo["created_at"])
    except (ValueError, TypeError):
        pytest.fail("created_at is not a valid ISO format string.")

    # Check if it was added to the list
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo

def test_list_todos():
    """
    Tests if list_todos returns all added items.
    """
    # Initially, the list should be empty
    assert storage.list_todos() == []

    # Add some todos
    todo1 = storage.add_todo("Task 1")
    todo2 = storage.add_todo("Task 2")

    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos

def test_delete_todo_success():
    """
    Tests if deleting an existing todo returns True and removes it from the list.
    """
    todo = storage.add_todo("To be deleted")
    todo_id = todo["id"]

    # The list should have one item before deletion
    assert len(storage.list_todos()) == 1

    # Delete the todo
    result = storage.delete_todo(todo_id)

    # Check if deletion was successful
    assert result is True
    assert len(storage.list_todos()) == 0

def test_delete_todo_not_found():
    """
    Tests that attempting to delete a non-existent todo returns False.
    """
    storage.add_todo("An existing todo")

    # Attempt to delete a todo with an ID that does not exist
    result = storage.delete_todo(999)

    assert result is False
    # Ensure the list was not modified
    assert len(storage.list_todos()) == 1

def test_id_auto_increments_correctly():
    """
    Tests that IDs auto-increment correctly, even after a deletion.
    IDs should be 1, 2, 3. Delete 2. Add new. IDs should be 1, 3, 4.
    """
    # Add three todos
    t1 = storage.add_todo("Task 1")
    t2 = storage.add_todo("Task 2")
    t3 = storage.add_todo("Task 3")

    assert t1["id"] == 1
    assert t2["id"] == 2
    assert t3["id"] == 3

    # Delete the middle todo
    storage.delete_todo(2)

    # Add another todo
    t4 = storage.add_todo("Task 4")

    # The new todo should have the next ID in sequence (4)
    assert t4["id"] == 4

    # Verify the final list of IDs
    current_ids = [todo["id"] for todo in storage.list_todos()]
    assert current_ids == [1, 3, 4]

```

## Decisions Made
1.  **`requirements.txt` Content**: Since the content of `requirements.txt` was not provided, I created a plausible file based on the repository context. I included `ghapi` and `openai` (inferred from `src/` files) and `pytest` for testing, in addition to the newly required `pydantic`. This provides a complete and runnable context.
2.  **`delete_todo` Implementation**: I chose to implement `delete_todo` using a list comprehension (`todos = [t for t in todos if t.get("id") != todo_id]`). This approach is concise, pythonic, and safely rebuilds the list without the risk of modification-during-iteration errors. The function's success is determined by comparing the list length before and after the operation.
3.  **Timestamp Format Validation**: In `tests/test_storage.py`, I used `datetime.fromisoformat()` within a `try...except` block to validate that the `created_at` field is a valid ISO 8601 string, as this is a robust way to confirm the format.
4.  **Test Isolation Fixture**: I implemented the `reset_storage` fixture with `autouse=True` and made it teardown the storage as well by clearing the list and resetting the counter after the test yields. This ensures maximum test isolation.

## Notes
-   The new `webapp` functionality is self-contained and does not interact with the existing `src` code.
-   The in-memory storage in `webapp/storage.py` is not thread-safe. For a concurrent application (e.g., a multi-threaded web server), access to the module-level `todos` list and `_next_id` counter would need to be protected by a lock (e.g., `threading.Lock`).
-   The project structure was followed by creating new files in their respective required locations (`webapp/` and `tests/`). The `webapp` directory itself would need to be created if it doesn't exist.
