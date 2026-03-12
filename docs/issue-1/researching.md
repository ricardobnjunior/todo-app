# RESEARCHING - Issue #1

## Research Findings
### Pydantic Model with Automatic Timestamps
Pydantic is a data validation library that uses Python type hints. To create a model with an automatically generated field like `created_at`, Pydantic's `Field` with a `default_factory` is the standard and recommended practice.

The `default_factory` should be a callable that returns the desired value. For an ISO-formatted UTC timestamp, the `datetime` standard library is ideal. The best practice is to use `datetime.now(timezone.utc).isoformat()`. Using `timezone.utc` ensures the timestamp is timezone-aware and unambiguous, avoiding common issues with local timezones.

Example:
```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Todo(BaseModel):
    id: int
    title: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
```

This approach encapsulates the default value logic within the data model itself, making it more robust and reusable.

### In-Memory Storage Pattern
For simple applications, a common pattern for in-memory storage is to use module-level variables. Python modules are singletons, so any variables defined at the top level of a module (`storage.py` in this case) will be created only once and shared across all parts of the application that import that module.

The requested design uses a `list` for the collection and a separate integer for the ID counter. This is a straightforward implementation.
- `todos: list[dict] = []` will serve as the database table.
- `_next_id: int = 1` will act as a simple auto-incrementing primary key sequence. The leading underscore correctly signals that it's intended for internal use within the module.

Operations on these shared variables (like `add_todo` and `delete_todo`) should be handled by functions within the same module to encapsulate the logic and control access.

### Testing State-Dependent Modules
When testing a module that maintains a global state (like our in-memory storage), it is crucial to ensure test isolation. Each test function should run with a clean, predictable state, independent of other tests.

A standard way to achieve this with `pytest` is to use fixtures and `monkeypatch`. A fixture can be defined to run before each test, using `monkeypatch.setattr` to reset the module-level variables (`todos` and `_next_id`) to their initial values.

Example fixture in `tests/test_storage.py`:
```python
import pytest
from webapp import storage

@pytest.fixture(autouse=True)
def reset_storage():
    """Reset the in-memory storage before each test."""
    storage.todos.clear()
    storage._next_id = 1
```
The `autouse=True` argument makes this fixture automatically apply to all tests in the file, ensuring consistent state management without boilerplate in every test function.

## Duplication Check
The repository does not contain any existing data models using Pydantic, nor does it have an in-memory CRUD (Create, Read, Update, Delete) storage system. The existing code in `src/` is focused on orchestrating interactions with LLMs and the GitHub API.

- `src/github_client.py` and other files return `list[dict]`, which is consistent with the return types requested for the new storage functions.
- The `dashboard/app.py` file contains a function `_parse_dt` which uses `datetime.fromisoformat`. This shows a preference for ISO 8601 datetime strings in the project, aligning with the proposed implementation for `created_at`.
- The testing patterns in `tests/` (e.g., helper functions for data creation, use of `pytest`) provide a good template for `tests/test_storage.py`.

Given that the `webapp` component is entirely new and functionally distinct from the existing agent logic, there is no code to be reused or refactored. The implementation will be completely new.

## Recommended Approach
1.  **Dependency Management**: Add `pydantic` to the `requirements.txt` file.
2.  **Directory Structure**: Create the new `webapp/` directory and an empty `webapp/__init__.py` file to mark it as a Python package.
3.  **Data Model (`webapp/models.py`)**: Implement the `Todo` model using `pydantic.BaseModel`. Use `Field(default_factory=...)` to automatically generate the `created_at` timestamp as a UTC ISO 8601 string. This keeps the model self-contained and descriptive.
4.  **Storage Layer (`webapp/storage.py`)**:
    *   Implement the module-level `todos: list[dict]` and `_next_id: int`.
    *   In `add_todo(title: str) -> dict`, create a `Todo` model instance. This will handle validation and default value generation. Then, convert the model to a dictionary using `.model_dump()` (for Pydantic v2) or `.dict()` (for Pydantic v1) before appending it to the `todos` list. This fulfills the requirement of storing and returning `dict` objects while still leveraging Pydantic's power.
    *   In `delete_todo(todo_id: int)`, iterate through the `todos` list to find the item with the matching `id`. A safe way to remove the item is to find its index and use `del storage.todos[index]`, or to rebuild the list with a list comprehension `todos[:] = [t for t in todos if t['id'] != todo_id]`. The latter is generally safer and more readable.
5.  **Testing (`tests/test_storage.py`)**:
    *   Create `tests/test_storage.py`.
    *   Implement a `pytest` fixture with `autouse=True` to reset the storage state before each test, ensuring test isolation.
    *   Write specific tests covering all requirements: adding, listing, deleting an existing item, deleting a non-existent item, and verifying the auto-incrementing ID logic, especially after a deletion.

## Risks and Edge Cases
-   **Concurrency**: The proposed module-level storage is not thread-safe. If the application were to be used in a multi-threaded environment (e.g., a web server with multiple workers), race conditions could occur when modifying `todos` or `_next_id`. For this simple application, this is not a concern, but for a production system, a `threading.Lock` would be required around write operations (`add_todo`, `delete_todo`).
-   **Data Volatility**: The in-memory storage is ephemeral. All data will be lost on application restart. This is expected per the issue description but is a critical limitation to be aware of.
-   **Test State Leakage**: Failure to properly isolate tests can lead to flaky and unreliable test suites. Using a `pytest` fixture to reset the state is crucial to mitigate this risk.
-   **Model vs. Dictionary**: The requirements specify that the storage functions should return `dict`s, not `Todo` model instances. This means consumers of the storage layer lose the benefits of static type checking that the Pydantic model provides. The recommended approach of using the model for creation/validation and then converting to a dict balances the requirements with good practice.
-   **Deletion Logic**: Care must be taken in `delete_todo`. Modifying a list while iterating over it can lead to bugs. Rebuilding the list via a list comprehension or finding the element's index first before deleting are safer alternatives to using `list.remove()` in a loop.

## Sources
-   Pydantic Documentation: Field with `default_factory` - [https://docs.pydantic.dev/latest/usage/fields/#default_factory](https://docs.pydantic.dev/latest/usage/fields/#default_factory)
-   Python `datetime` Documentation: `isoformat()` and `timezone` - [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
-   `pytest` Documentation: `monkeypatch` and fixtures - [https://docs.pytest.org/en/stable/how-to/monkeypatch.html](https://docs.pytest.org/en/stable/how-to/monkeypatch.html), [https://docs.pytest.org/en/stable/how-to/fixtures.html](https://docs.pytest.org/en/stable/how-to/fixtures.html)
