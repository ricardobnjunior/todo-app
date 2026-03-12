# RESEARCHING - Issue #1

## Research Findings
### Pydantic Model and Datetime Generation
The issue requires a Pydantic model `Todo` with an automatically generated `created_at` timestamp in ISO format. The best practice for this is to use Pydantic's `Field` with a `default_factory`.

To generate a timezone-aware ISO 8601 timestamp, the standard library `datetime` is the best choice. The recommended approach is `datetime.now(timezone.utc).isoformat()`. Using `timezone.utc` ensures the timestamp is not naive and is standardized, which prevents issues with localization and time zones.

Example:
```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Todo(BaseModel):
    id: int
    title: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
```
This sets the `created_at` field to the current UTC time in ISO format whenever a new `Todo` instance is created without an explicit `created_at` value.

### In-Memory Storage Pattern
For simple applications or testing, module-level variables for storage are a common and straightforward pattern. The requirements specify a `list` for the data and an `int` for an ID counter.

- **ID Generation:** A simple global counter (`_next_id`) that is incremented upon each creation is sufficient for this use case.
- **Data Manipulation:**
    - `add_todo`: Should create a data structure (in this case, a dict), append it to the global list, and return it. It's good practice to use the Pydantic model to create the object and then convert it to a dictionary (using `model.model_dump()` in Pydantic v2) to ensure data consistency and validation.
    - `list_todos`: To ensure the internal storage list is not accidentally modified by consumers of the function, it should return a *copy* of the list (e.g., `todos.copy()` or `todos[:]`).
    - `delete_todo`: A safe way to remove an item from a list is to rebuild the list, excluding the item to be deleted. A list comprehension like `todos[:] = [t for t in todos if t['id'] != todo_id]` is efficient and avoids mutation-during-iteration errors. The function should return `True` or `False` based on whether an item was actually removed.

### TDD with Pytest
The project already uses `pytest`. The new tests should follow existing conventions. For testing stateful modules like `storage.py`, it is crucial to ensure tests are isolated. A `pytest` fixture with `autouse=True` is the ideal mechanism to reset the storage state (the `todos` list and `_next_id` counter) before each test function runs. This prevents the outcome of one test from affecting another.

Example of a reset fixture:
```python
import pytest
from webapp import storage

@pytest.fixture(autouse=True)
def reset_storage():
    """Resets storage before each test."""
    storage.todos.clear()
    storage._next_id = 1
```

## Duplication Check
The repository does not contain any code similar to the requested `webapp` component. The `src/` directory contains logic for a GitHub agent orchestrator, which is a completely different domain. The project uses `list[dict]` in places like `src/github_client.py` and `dashboard/app.py`, but this is for holding data fetched from APIs, not for an in-memory storage layer with Create/Read/Delete operations. No Pydantic models or similar data layer patterns exist.

Therefore, the new files (`webapp/__init__.py`, `webapp/models.py`, `webapp/storage.py`, `tests/test_storage.py`) will be entirely new implementations and will not duplicate existing logic. The primary reusable aspect is the testing style and conventions established in the `tests/` directory.

## Recommended Approach
1.  **Create `webapp` package**: Start by creating the `webapp` directory and an empty `webapp/__init__.py` file to make it a Python package.

2.  **`webapp/models.py`**:
    -   Define the `Todo` class inheriting from `pydantic.BaseModel`.
    -   Use `Field` with `default_factory` for the `created_at` field to automatically generate a UTC ISO timestamp as researched. This encapsulates the data structure's logic cleanly.

3.  **`webapp/storage.py`**:
    -   Initialize the module-level `todos: list[dict] = []` and `_next_id: int = 1`.
    -   **`add_todo(title: str)`**:
        -   Inside the function, create an instance of the `Todo` model from `webapp.models`: `new_todo_model = Todo(id=_next_id, title=title)`. This leverages the Pydantic model for data creation and validation (e.g., `created_at` generation).
        -   Increment `_next_id`.
        -   Convert the Pydantic model to a dictionary using `new_todo_model.model_dump()`.
        -   Append this dictionary to the `todos` list.
        -   Return the dictionary.
    -   **`list_todos()`**: Return `todos.copy()` to prevent direct mutation of the internal state.
    -   **`delete_todo(todo_id: int)`**:
        -   Store the initial length of the `todos` list.
        -   Use `todos[:] = [t for t in todos if t['id'] != todo_id]` to remove the item in-place.
        -   Return `len(todos) < initial_length` to indicate if a deletion occurred.

4.  **`tests/test_storage.py`**:
    -   Create a new test file `tests/test_storage.py`.
    -   Implement a `pytest` fixture with `autouse=True` to reload/reset the `webapp.storage` module's state before each test.
    -   Write separate test functions for each requirement: adding, listing, deleting an existing item, deleting a non-existent item, and verifying the ID auto-increment logic.
    -   In `test_add_todo`, validate the format of the `created_at` string using `datetime.fromisoformat()`.

5.  **Dependencies**: Add `pydantic` to the `requirements.txt` file.

This approach fulfills all requirements, follows best practices, and introduces a clean, well-tested, and encapsulated data layer.

## Risks and Edge Cases
-   **Thread Safety**: The proposed in-memory storage is not thread-safe. Concurrent calls to `add_todo` or `delete_todo` could lead to race conditions (e.g., duplicate IDs, lost data). For this simple application, this is likely an acceptable risk. For a production system, a `threading.Lock` would be necessary to protect access to `todos` and `_next_id`.
-   **Data Persistence**: In-memory storage is volatile. The entire todo list will be lost if the application restarts. This is inherent to the "in-memory" requirement but is a key limitation to be aware of.
-   **Returning Mutable Objects**: The `list_todos` function must return a copy of the list. If it returns a reference to the internal list, a consumer could modify it, breaking encapsulation. The recommended approach (`todos.copy()`) mitigates this.
-   **Test State Bleeding**: Without proper test isolation (the `pytest` fixture), the stateful nature of the `storage` module will cause tests to fail intermittently by depending on the order of execution. The `autouse` fixture is critical to prevent this.

## Sources
-   Pydantic Documentation - Field `default_factory`: [https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.Field](https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.Field)
-   Pydantic Documentation - Model `model_dump()`: [https://docs.pydantic.dev/latest/api/base_model/#pydantic.main.BaseModel.model_dump](https://docs.pydantic.dev/latest/api/base_model/#pydantic.main.BaseModel.model_dump)
-   Python `datetime` Documentation - `isoformat()` and `timezone`: [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
-   `pytest` Fixtures Documentation: [https://docs.pytest.org/en/stable/how-to/fixtures.html](https://docs.pytest.org/en/stable/how-to/fixtures.html)
