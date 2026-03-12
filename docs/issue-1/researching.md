# RESEARCHING - Issue #1

## Research Findings
### Pydantic Model Definition
Pydantic is a data validation and settings management library. A `BaseModel` can be used to define the `Todo` data structure. For fields that need to be automatically generated, like `created_at`, Pydantic's `Field` with a `default_factory` is the standard approach.

For the `created_at` field, a function that returns the current time as an ISO-formatted string is required. The `datetime` module from the standard library is perfect for this. Using `datetime.now(timezone.utc)` is a best practice to generate timezone-aware timestamps, avoiding ambiguity. The `.isoformat()` method then serializes this `datetime` object into the required string format.

Example Pydantic model structure:
```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def get_current_time_iso():
    return datetime.now(timezone.utc).isoformat()

class Todo(BaseModel):
    id: int
    title: str
    created_at: str = Field(default_factory=get_current_time_iso)
```

### In-Memory Storage
Using module-level variables (`list` and `int`) is a straightforward way to implement simple in-memory storage. This pattern is common for simple examples or prototypes.

The functions (`add_todo`, `list_todos`, `delete_todo`) will manipulate these global variables.
- `add_todo`: Should create a Pydantic model instance to leverage its validation and default value generation, then convert it to a dictionary for storage using `.model_dump()`.
- `list_todos`: Should return a *copy* of the list (e.g., `todos[:]`) to prevent callers from accidentally modifying the internal state.
- `delete_todo`: Needs to iterate through the list to find the item to remove. Using `next()` with a generator is an efficient way to find the first matching item.

### Testing State-Dependent Modules
When testing modules with global state (like our `storage` module), tests are not isolated by default. One test's actions (e.g., adding a todo) will affect the state available to the next test. The standard solution in `pytest` is to use a fixture with `autouse=True` to reset the state before each test runs. This ensures each test starts with a clean slate.

Example fixture:
```python
import pytest
from webapp import storage

@pytest.fixture(autouse=True)
def reset_storage():
    """Reset the in-memory storage before each test."""
    storage.todos.clear()
    storage._next_id = 1
```

## Duplication Check
The repository does not contain any code related to a "ToDo" application or a similar CRUD (Create, Read, Update, Delete) in-memory storage system. The existing code is focused on orchestrating a GitHub workflow with an LLM agent.

- **Data Models:** The project currently uses plain `dict` and `list[dict]` for data transfer (e.g., `github_client.list_agent_issues`). The introduction of a Pydantic model in `webapp/models.py` will be a new pattern for formal data definition.
- **Storage:** There is no existing in-memory database or storage layer. The current logic either interacts with external APIs (GitHub) or reads from the filesystem (`repo_context.py`).
- **Web Application:** The `webapp` directory is entirely new and does not overlap with `src`, `dashboard`, or `tests`.

Given the lack of similar functionality, the implementation will be entirely new code. The new code should, however, follow the existing coding style, such as using type hints and `snake_case` naming conventions.

## Recommended Approach
1.  **Create `webapp/__init__.py`:** An empty file to make `webapp` a package.
2.  **Create `webapp/models.py`:** Define the `Todo` class using `pydantic.BaseModel`. Use `Field(default_factory=...)` to automatically generate the `created_at` timestamp in UTC ISO format. This centralizes data validation and default value logic.
3.  **Create `webapp/storage.py`:**
    -   Initialize the module-level `todos: list[dict] = []` and `_next_id: int = 1`.
    -   In `add_todo`, instantiate the `Todo` model with the `id` and `title`, then call `.model_dump()` to get a dictionary. Append this dictionary to the `todos` list. This approach ensures all created todos are valid according to the model.
    -   In `delete_todo`, iterate to find the dictionary with the matching `todo_id`. If found, remove it from the list and return `True`; otherwise, return `False`.
4.  **Create `tests/test_storage.py`:**
    -   Implement a `pytest` fixture with `autouse=True` to reset the `todos` list and `_next_id` counter before each test, ensuring test isolation.
    -   Write specific test functions to cover all requirements: adding, listing, deleting (both successful and unsuccessful cases), and verifying the ID auto-increment logic, especially after a deletion.
5.  **Update `requirements.txt`:** Add `pydantic` as a new dependency.

This approach adheres to the requirements while leveraging best practices for data validation (Pydantic), test isolation (`pytest` fixtures), and handling timestamps (UTC).

## Risks and Edge Cases
-   **Test Isolation:** This is the most significant risk. If the module-level storage is not reset between tests, test outcomes will become dependent on their execution order, leading to flaky and unreliable tests. An `autouse` fixture is critical to mitigate this.
-   **Concurrency:** The use of module-level globals (`todos`, `_next_id`) makes the storage layer not thread-safe. In a multi-threaded web server, concurrent requests to `add_todo` could lead to a race condition where two todos are assigned the same ID. While likely not an issue for this simple application, for a real-world scenario, a `threading.Lock` would be necessary around any read/write operations on the shared state.
-   **Data Volatility:** The in-memory storage is ephemeral and will be lost on application restart. This is an explicit requirement but a critical limitation to be aware of.
-   **Deletion Logic:** When deleting an item from a list while iterating over it, care must be taken. The recommended approach of finding the item first and then calling `list.remove(item)` is safe. Modifying the list directly within a loop can lead to skipping items.
-   **Timezone:** Not specifying a timezone for `datetime.now()` can lead to inconsistencies depending on the server's local time. Using `datetime.now(timezone.utc)` is a robust practice that should be adopted.

## Sources
-   **Pydantic Documentation:** [https://docs.pydantic.dev/latest/usage/models/](https://docs.pydantic.dev/latest/usage/models/)
-   **Pydantic Fields and default_factory:** [https://docs.pydantic.dev/latest/usage/fields/#default_factory](https://docs.pydantic.dev/latest/usage/fields/#default_factory)
-   **Python `datetime` module:** [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
-   **`pytest` Fixtures:** [https://docs.pytest.org/en/stable/how-to/fixtures.html](https://docs.pytest.org/en/stable/how-to/fixtures.html)
