# RESEARCHING - Issue #1

## Research Findings
### Pydantic Models
Pydantic is a data validation and settings management library. A `BaseModel` is used to define a data object's schema.

For automatically generated fields like `created_at`, Pydantic's `Field` function with `default_factory` is the standard practice. This factory is a zero-argument callable that returns the default value when a new model instance is created without that field being provided.

Example:
```python
from pydantic import BaseModel, Field
from datetime import datetime, timezone

def get_utc_now_iso_string():
    return datetime.now(timezone.utc).isoformat()

class MyModel(BaseModel):
    id: int
    created_at: str = Field(default_factory=get_utc_now_iso_string)
```

### Datetime Handling
To generate an ISO format datetime string, Python's built-in `datetime` library is sufficient. Best practice is to use timezone-aware datetimes to avoid ambiguity. `datetime.now(timezone.utc)` creates a timezone-aware object for the current time in UTC. The `.isoformat()` method then serializes this to a string compliant with the ISO 8601 standard (e.g., `2023-10-27T10:30:00.123456+00:00`). Using `datetime.utcnow()` is discouraged as it produces a "naive" datetime object without timezone information.

### In-Memory Storage
Using module-level variables (`list`, `int`) is a straightforward way to implement simple in-memory storage for non-production or demo applications. A key consideration is that these variables constitute a global state.

When modifying a module-level variable from within a function, the `global` keyword must be used. For example:
```python
_counter = 0

def increment():
    global _counter
    _counter += 1
```

### Testing State-dependent Modules
Testing code with module-level state requires careful management to ensure test isolation. If the state is not reset between tests, the outcome of one test can affect another, leading to flaky and unreliable test suites.

The idiomatic way to handle this in `pytest` is to use a fixture with `autouse=True`. This fixture runs automatically before each test function in its scope (e.g., module), resetting the state to a known baseline.

Example:
```python
# in tests/test_storage.py
import pytest
from webapp import storage

@pytest.fixture(autouse=True)
def reset_storage_state():
    """Resets the in-memory storage before each test."""
    storage.todos.clear()
    global _next_id
    storage._next_id = 1
```

## Duplication Check
The codebase does not contain any existing application data models or a storage layer. The `src/` directory is focused on the agent orchestration logic (interacting with GitHub, LLMs, etc.), and `dashboard/` is for a separate monitoring tool. The new `webapp/` component is a distinct feature with no direct overlap.

However, the pattern of using `list[dict]` to pass collections of data is common throughout the project (e.g., `src/github_client.py:list_agent_issues`, `dashboard/app.py:fetch_pull_requests`). The request for the `storage.py` functions to operate on dictionaries aligns with this existing pattern, even though a Pydantic model is used for defining the schema.

Test structure in `tests/` consistently uses `pytest`, `test_*.py` file naming, and helper functions for setup, which should be followed for `tests/test_storage.py`.

## Recommended Approach
1.  **`webapp/__init__.py`**: Create this empty file to define the `webapp` directory as a Python package.

2.  **`webapp/models.py`**: Define the `Todo` model using `pydantic.BaseModel`. Use `Field(default_factory=...)` for the `created_at` field to automatically generate the timestamp upon model creation. While the storage functions will work with `dict`s, this model will serve as the single source of truth for the data structure, useful for validation in an API layer later.
    ```python
    # In webapp/models.py
    from pydantic import BaseModel, Field
    from datetime import datetime, timezone

    class Todo(BaseModel):
        id: int
        title: str
        created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ```

3.  **`webapp/storage.py`**:
    *   Implement the module-level list `todos: list[dict] = []` and counter `_next_id: int = 1`.
    *   In `add_todo(title: str)`, use the `global` keyword to modify `_next_id`. Manually create the `created_at` timestamp using `datetime.now(timezone.utc).isoformat()` to keep the function self-contained and adhere to the `-> dict` return type hint. This avoids instantiating a Pydantic model just to convert it back to a `dict`.
    *   In `delete_todo(todo_id: int)`, find the todo by looping through the list. To safely remove it, find the item first and then use `todos.remove(item_to_remove)` or find its index and use `del todos[index]`. A list comprehension (`todos[:] = [t for t in todos if t['id'] != todo_id]`) is also a robust method.
    *   In `list_todos()`, return `todos.copy()` to prevent external consumers from accidentally modifying the internal storage list.

4.  **`tests/test_storage.py`**:
    *   Create a `pytest` fixture with `autouse=True` at the top of the file to reset the `storage.todos` list and `storage._next_id` counter before each test function runs. This is critical for test isolation.
    *   Write separate test functions for each requirement outlined in the issue: adding, listing, deleting (success and failure cases), and verifying the ID auto-increment logic.

## Risks and Edge Cases
*   **Test State Leakage**: The biggest risk is that tests interfere with each other due to the shared module-level state. A `pytest` fixture to reset the state before each test is essential to mitigate this.
*   **Concurrency**: The proposed in-memory storage is not thread-safe. Concurrent calls to `add_todo` could lead to a race condition and duplicate IDs. While this is likely out of scope for the current issue, it's a known limitation of this simple pattern. A `threading.Lock` would be needed to make it thread-safe.
*   **Inconsistent Data**: The `storage.py` functions create dictionaries manually. It is possible for their implementation to drift out of sync with the `Todo` Pydantic model. The tests should assert the structure of the returned dictionaries to catch such regressions.
*   **Datetime Timezones**: Care must be taken to use timezone-aware datetimes (`datetime.now(timezone.utc)`) to produce correct ISO 8601 strings. Using the naive `datetime.utcnow()` can lead to subtle bugs.

## Sources
*   [Pydantic Docs - Field with `default_factory`](https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.Field)
*   [Python Docs - `datetime` module](https://docs.python.org/3/library/datetime.html)
*   [Pytest Docs - Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
*   [Pytest Docs - `autouse` fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html#autouse-fixtures-apply-fixtures-to-all-tests-in-a-module)
