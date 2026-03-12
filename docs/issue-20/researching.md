# RESEARCHING - Issue #20

## Research Findings
### Pydantic Model with Auto-generated Timestamp
Pydantic is the standard library for data validation in modern Python. For the `Todo` model, the requirements are:
- `id: int`
- `title: str`
- `created_at: str` (ISO format, auto-generated)

To achieve the auto-generated timestamp, Pydantic's `Field` with a `default_factory` is the best practice. The factory will be a function that generates the current time. It is crucial to use timezone-aware datetimes to avoid ambiguity. The recommended approach is `datetime.datetime.now(datetime.timezone.utc)`. The `.isoformat()` method can then be called on the resulting `datetime` object to produce the required string representation.

Example:
```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def get_utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

class Todo(BaseModel):
    id: int
    title: str
    created_at: str = Field(default_factory=get_utc_now_iso)
```
Using a lambda function directly in the `default_factory` is also a common and concise pattern: `default_factory=lambda: datetime.now(timezone.utc).isoformat()`.

### In-Memory Storage
Using module-level variables for simple in-memory storage is a straightforward pattern for small applications or prototypes. The state is managed within a single Python module.

- **Data Structure**: The issue requires a `list[dict]` for storage. While a `dict` keyed by `todo_id` would offer more performant lookups and deletions (O(1) vs. O(n)), adhering to the specified `list[dict]` is necessary.
- **ID Generation**: A module-level integer counter (`_next_id`) is a simple way to ensure unique, auto-incrementing IDs. It's important to declare the variable as `global` within the `add_todo` function to modify it.
- **Data Conversion**: Although the Pydantic model defines the data structure, the storage functions are required to work with and return plain dictionaries. Pydantic model instances can be converted to dictionaries using the `.model_dump()` method (in Pydantic v2) or `.dict()` (in v1). This keeps the storage layer decoupled from the specific model implementation.

### Testing In-Memory State
When testing components with in-memory state, it is critical to ensure test isolation. State from one test must not leak into another. For pytest, there are two common approaches:
1.  **Fixtures with monkeypatching**: A pytest fixture can use the built-in `monkeypatch` fixture to reset the state variables (e.g., `storage.todos = []`, `storage._next_id = 1`) before each test runs.
2.  **Module reloading**: A fixture can use `importlib.reload()` on the storage module. This effectively re-executes the module-level code, resetting all variables to their initial state. This is often cleaner than patching multiple variables.

## Duplication Check
The repository does not contain any existing data models or in-memory storage systems similar to what is required for the `webapp`.

- The `src/` directory contains the logic for an AI agent orchestrator that interacts with the GitHub API. Functions like `list_agent_issues` in `src/github_client.py` return a `list[dict]`, which is a similar data structure, but the data originates from an external API call, and there is no local storage or mutation logic.
- The `dashboard/` directory contains a Streamlit application that also fetches and displays data but does not implement a persistent or mutable data layer.
- Other parts of the codebase deal with file system traversal, API clients, and running processes.

Conclusion: This is a net-new feature. The new `webapp` package and its modules (`models.py`, `storage.py`) will be created from scratch. The implementation should, however, follow the existing coding conventions (type hints, `snake_case`, etc.).

## Recommended Approach
1.  **`webapp/__init__.py`**: Create this empty file to establish `webapp` as a Python package.

2.  **`webapp/models.py`**:
    - Define a `Todo` class inheriting from `pydantic.BaseModel`.
    - Use `Field(default_factory=...)` for the `created_at` field to automatically generate a UTC-based ISO 8601 timestamp upon model instantiation. This encapsulates the timestamp generation logic within the model definition.

3.  **`webapp/storage.py`**:
    - Implement the module-level `todos: list[dict] = []` and `_next_id: int = 1`.
    - In `add_todo(title: str)`, use the `global _next_id` statement. Instantiate the `Todo` model from `webapp.models` with the next ID and the provided title. The `created_at` field will be populated automatically.
    - Convert the `Todo` instance to a dictionary using `.model_dump()` before appending it to the `todos` list and returning it.
    - In `delete_todo(todo_id: int)`, iterate through the `todos` list to find the item. A list comprehension to find the index or object is suitable. If found, use `list.remove()` to delete it and return `True`. If not found, return `False`.
    - In `list_todos()`, return a copy of the list (`todos[:]`) to prevent consumers from accidentally modifying the internal state.

4.  **`tests/test_storage.py`**:
    - Use `pytest` for testing.
    - Create a pytest fixture that uses `importlib.reload(webapp.storage)` to ensure the in-memory database is reset before each test function execution. Apply this fixture to all tests in the file.
    - Write separate test functions to cover each case outlined in the issue: adding, listing, deleting an existing item, deleting a non-existent item, and verifying the auto-increment logic for IDs.

5.  **`requirements.txt`**: Add `pydantic` as a new dependency.

This approach directly fulfills all requirements of the issue while adhering to best practices for data modeling, state management in tests, and date/time handling.

## Risks and Edge Cases
- **Test State Contamination**: The biggest risk is state leakage between tests. If the storage module is not reset before each test, test results will be inconsistent and dependent on execution order. Using a pytest fixture to reload the module is crucial to mitigate this.
- **Concurrency Issues**: The proposed in-memory storage is not thread-safe. If the application were to be used in a multi-threaded environment, simultaneous calls to `add_todo` could lead to a race condition where two todos are assigned the same ID. While this is out of scope for the current issue, it is a key architectural limitation to be aware of. Adding a `threading.Lock` around modifications to `_next_id` and the `todos` list would be the solution.
- **Data Volatility**: Since the storage is in-memory, all data will be lost when the application process terminates. This is per the requirements but means the feature is not suitable for production use without a persistent storage backend (like a database or file).

## Sources
- Pydantic Documentation - Fielåds: [https://docs.pydantic.dev/latest/api/fields/](https://docs.pydantic.dev/latest/api/fields/)
- Pydantic Documentation - `default_factory`: [https://docs.pydantic.dev/latest/concepts/fields/#default_factory](https://docs.pydantic.dev/latest/concepts/fields/#default_factory)
- Python `datetime` Documentation (for `timezone` and `isoformat`): [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
- Pytest Documentation - Fixtures: [https://docs.pytest.org/en/stable/explanation/fixtures.html](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- Python `importlib` Documentation (for `reload`): [https://docs.python.org/3/library/importlib.html#importlib.reload](https://docs.python.org/3/library/importlib.html#importlib.reload)
