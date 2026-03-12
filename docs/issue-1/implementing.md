# IMPLEMENTING - Issue #1

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.
```

### FILE: requirements.txt
```
anthropic
python-dotenv
fastapi-poe
ghapi
pygithub
rich
pydantic
```

### FILE: webapp/models.py
```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def _generate_utc_iso_string() -> str:
    """
    Generates the current time in UTC as an ISO 8601 formatted string.
    """
    return datetime.now(timezone.utc).isoformat()


class Todo(BaseModel):
    """
    Represents a single ToDo task.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=_generate_utc_iso_string)

```

### FILE: webapp/storage.py
```python
from typing import TypedDict, List
from .models import Todo

# An in-memory storage for todos.
# For a real application, this would be replaced with a database.

class TodoDict(TypedDict):
    """
    A dictionary representation of a Todo item, for type hinting.
    """
    id: int
    title: str
    created_at: str

todos: List[TodoDict] = []
_next_id: int = 1

def add_todo(title: str) -> TodoDict:
    """
    Creates a new todo, adds it to the in-memory list, and returns it.

    Args:
        title: The title of the todo task.

    Returns:
        The newly created todo as a dictionary.
    """
    global _next_id
    new_todo_model = Todo(id=_next_id, title=title)
    new_todo_dict = new_todo_model.model_dump()

    todos.append(new_todo_dict)
    _next_id += 1
    
    return new_todo_dict

def list_todos() -> List[TodoDict]:
    """
    Returns a copy of the list of all todos.

    Returns:
        A list of todo dictionaries.
    """
    return todos.copy()

def delete_todo(todo_id: int) -> bool:
    """
    Deletes a todo by its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was deleted, False otherwise.
    """
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return len(todos) < initial_length

```

### FILE: tests/test_storage.py
```python
from datetime import datetime
import pytest
from webapp import storage, models

@pytest.fixture(autouse=True)
def reset_storage_state():
    """
    This fixture automatically runs before each test function.
    It resets the in-memory storage to a clean state, ensuring
    that tests are isolated and don't interfere with each other.
    """
    storage.todos.clear()
    storage._next_id = 1


def test_add_todo_returns_correct_structure():
    """
    Tests that add_todo creates a todo with the correct structure and data.
    """
    title = "My First Task"
    new_todo = storage.add_todo(title)

    assert isinstance(new_todo, dict)
    assert 'id' in new_todo
    assert 'title' in new_todo
    assert 'created_at' in new_todo

    assert new_todo['id'] == 1
    assert new_todo['title'] == title

    # Verify that created_at is a valid ISO 8601 timestamp string
    try:
        datetime.fromisoformat(new_todo['created_at'])
    except (ValueError, TypeError):
        pytest.fail("created_at is not a valid ISO 8601 string.")

    # Verify the todo was actually added to the list
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos_returns_all_items():
    """
    Tests that list_todos returns all items that have been added.
    """
    storage.add_todo("Task 1")
    storage.add_todo("Task 2")
    storage.add_todo("Task 3")

    all_todos = storage.list_todos()
    assert len(all_todos) == 3
    assert all_todos[0]['title'] == "Task 1"
    assert all_todos[1]['id'] == 2
    assert all_todos[2]['title'] == "Task 3"


def test_delete_existing_todo():
    """
    Tests that delete_todo correctly removes an existing item and returns True.
    """
    todo1 = storage.add_todo("Task to be deleted")
    storage.add_todo("Task to keep")

    # Delete the first todo
    result = storage.delete_todo(todo1['id'])
    
    assert result is True

    # Verify it was removed
    remaining_todos = storage.list_todos()
    assert len(remaining_todos) == 1
    assert remaining_todos[0]['title'] == "Task to keep"


def test_delete_non_existent_todo():
    """
    Tests that delete_todo returns False when trying to delete an item that does not exist.
    """
    storage.add_todo("An existing task")

    # Try to delete a todo with an ID that doesn't exist
    result = storage.delete_todo(999)

    assert result is False

    # Verify the list remains unchanged
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0]['title'] == "An existing task"


def test_id_auto_increment_after_deletion():
    """
    Tests that the auto-incrementing ID continues from the last value,
    even after items have been deleted.
    """
    # Add three todos, they should get IDs 1, 2, 3
    storage.add_todo("Task 1")
    storage.add_todo("Task 2")
    storage.add_todo("Task 3")

    # Delete the middle todo (ID 2)
    deleted = storage.delete_todo(2)
    assert deleted is True

    # Add a new todo, it should get ID 4
    new_todo = storage.add_todo("Task 4")
    assert new_todo['id'] == 4
    
    # Verify the final state of the list
    final_todos = storage.list_todos()
    assert len(final_todos) == 3
    
    final_ids = [todo['id'] for todo in final_todos]
    assert final_ids == [1, 3, 4]

# Test for the model itself, just to be thorough.
def test_todo_model_defaults():
    """
    Tests that the Pydantic model correctly assigns default values.
    """
    todo = models.Todo(id=1, title="Test Title")
    
    assert todo.id == 1
    assert todo.title == "Test Title"
    assert isinstance(todo.created_at, str)
    
    # Check that the default factory produces a valid ISO timestamp
    try:
        datetime.fromisoformat(todo.created_at)
    except (ValueError, TypeError):
        pytest.fail("Default created_at is not a valid ISO 8601 string.")

```

## Decisions Made

-   **`webapp/__init__.py`**: Created as an empty file as per the standard Python convention to mark a directory as a package.
-   **`requirements.txt`**: I added `pydantic` to the end of the file. The original order of requirements was maintained.
-   **`webapp/models.py`**: I created a helper function `_generate_utc_iso_string` to pass to `default_factory`. This makes the `Todo` class definition slightly cleaner and more readable. It ensures the timestamp is always UTC.
-   **`webapp/storage.py`**:
    -   I used a `TypedDict` (`TodoDict`) to provide more specific type hints for the list of dictionaries. This improves static analysis and code clarity over a plain `list[dict]`.
    -   The `add_todo` function leverages the `Todo` model from `models.py` to create the object and then dumps it to a dictionary (`model_dump()`), ensuring validation rules (like the `created_at` factory) are applied before storage. This decouples the storage layer (which works with simple dicts) from the model implementation.
    -   The `delete_todo` function was implemented by rebuilding the list via a list comprehension, which is a safe and Pythonic way to remove items. It returns a boolean based on whether the list's length changed.
-   **`tests/test_storage.py`**:
    -   I used a `pytest` fixture with `autouse=True` to reset the state of `storage` before each test. This is crucial for test isolation, as `storage` is a stateful module. Instead of module reloading, I opted to directly clear the list and reset the counter, which is simpler and more reliable.
    -   The tests cover all specified scenarios: adding, listing, deleting an existing todo, attempting to delete a non-existent one, and verifying the ID auto-increment logic.
    -   I added a specific check in `test_add_todo` to validate that `created_at` is a valid ISO 8601 formatted string, making the test more robust.
    -   I added an extra, small test (`test_todo_model_defaults`) to directly verify the behavior of the Pydantic model itself, ensuring the `default_factory` for `created_at` works as expected.

## Notes

-   The new `webapp` directory is created at the top level of the project, as requested. This is separate from the existing `src` directory, suggesting a new, distinct component is being added to the project.
-   The in-memory storage is deliberately simple and is **not thread-safe**. In a concurrent environment (like a multi-threaded web server), this could lead to race conditions. For the scope of this issue, this is acceptable, but for a real-world application, locks (`threading.Lock`) would be required around modifications to `todos` and `_next_id`.
-   The storage is volatile and will be reset every time the application restarts. This is inherent to the "in-memory" requirement.
-   The creation of a `webapp` package might require adjustments to the Python path if/when this code is executed by an application runner. For now, the tests run correctly because pytest modifies the path to include the project root.
