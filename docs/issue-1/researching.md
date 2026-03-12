# RESEARCHING - Issue #1

## Research Findings
### Pydantic Model with Automatic Timestamps
For creating the `Todo` model, Pydantic's `BaseModel` is the standard. To automatically generate the `created_at` timestamp, Pydantic provides the `default_factory` argument for its `Field` function. The best practice is to use a lambda function that calls the appropriate `datetime` method.

For generating an ISO-formatted UTC timestamp, `datetime.datetime.now(datetime.timezone.utc).isoformat()` is the modern, timezone-aware approach available in Python 3. A simpler, though timezone-naive, alternative is `datetime.datetime.utcnow().isoformat()`. Given the requirement is just "ISO format", the timezone-aware version is more robust and considered a better practice.

To serialize the model instance into a dictionary for storage, the `.model_dump()` method (in Pydantic v2) or `.dict()` (in Pydantic v1) should be used.

### In-Memory Storage Pattern
Using module-level variables for a simple in-memory store is a straightforward pattern suitable for this application's requirements.
- A `list` will hold the data objects (as dictionaries).
- A separate `int` counter will manage unique IDs.

For functions that modify the shared state (`todos` list, `_next_id` counter), it's important to consider atomicity. For example, in `add_todo`, the ID should be fetched from the counter and the counter incremented as a single logical step before the new item is added to the list.

### Testing State-dependent Modules with Pytest
When testing modules that contain a global state (like our `storage.py`), tests can interfere with each other. A standard `pytest` pattern to handle this is to use a fixture with `autouse=True`. This fixture runs automatically before each test, resetting the module's state to a known baseline. This ensures each test is isolated and independent. For instance, the fixture would clear the `todos` list and reset the `_next_id` counter to its initial value.

The test for auto-incrementing IDs should explicitly verify the non-sequential but unique nature of IDs after a deletion, as described in the issue.

## Duplication Check
The codebase does not contain any existing data models using Pydantic, nor does it have an in-memory storage layer like the one requested. The `src/` directory is focused on a GitHub agent orchestrator, and its state management relies on external API calls (`github_client.py`). The `dashboard/` uses caching but not a persistent in-memory store.

Therefore, `webapp/models.py` and `webapp/storage.py` will be entirely new implementations.

While there is no direct code to reuse, the project has established patterns that should be followed:
- **Type Hinting:** All new functions and variables should have clear type hints (e.g., `list[dict]`, `-> bool`), which is consistent across the existing codebase.
- **Naming Convention:** `snake_case` is used for functions and variables.
- **Testing Structure:** The new tests in `tests/test_storage.py` should follow the `pytest`-based structure seen in other `tests/test_*.py` files.

## Recommended Approach
1.  **Create `webapp/__init__.py`**: An empty file to define the `webapp` directory as a Python package.
2.  **Create `webapp/models.py`**:
    -   Define a `Todo` class inheriting from `pydantic.BaseModel`.
    -   Use `id: int` and `title: str`.
    -   For `created_at: str`, use `Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())`. This requires `from datetime import datetime, timezone` and `from pydantic import Field`.
3.  **Create `webapp/storage.py`**:
    -   Define module-level `todos: list[dict] = []` and `_next_id: int = 1`.
    -   **`add_todo(title: str) -> dict`**:
        -   Declare `_next_id` as `global`.
        -   Create a `Todo` instance: `new_todo = Todo(id=_next_id, title=title)`. Pydantic will handle `created_at`.
        -   Increment the global counter: `_next_id += 1`.
        -   Convert the model to a dictionary: `todo_dict = new_todo.model_dump()`.
        -   Append `todo_dict` to the global `todos` list.
        -   Return `todo_dict`.
    -   **`list_todos() -> list[dict]`**:
        -   Return a copy of the list (`todos.copy()`) to prevent external callers from accidentally modifying the internal state.
    -   **`delete_todo(todo_id: int) -> bool`**:
        -   Find the todo to delete. A list comprehension is a safe way to rebuild the list: `original_len = len(todos); todos[:] = [t for t in todos if t['id'] != todo_id]`.
        -   Return `True` if an item was removed (`len(todos) < original_len`), otherwise return `False`.
4.  **Create `tests/test_storage.py`**:
    -   Import `pytest` and the `webapp.storage` module.
    -   Create a fixture to reset the state before each test:
        ```python
        @pytest.fixture(autouse=True)
        def reset_storage():
            # This function runs before each test
            webapp.storage.todos.clear()
            webapp.storage._next_id = 1
        ```
    -   Implement the tests as specified in the issue, covering adding, listing, deleting (existing and non-existent), and the ID auto-increment logic.
    -   Assert the structure of the returned `dict` from `add_todo`, and validate that `created_at` is a valid ISO timestamp string.
5.  **Update `requirements.txt`**: Add `pydantic`.

## Risks and Edge Cases
-   **Concurrency**: The proposed module-level storage is **not thread-safe**. If this were to be used in a multi-threaded web server, simultaneous calls to `add_todo` could cause a race condition, leading to duplicate IDs or lost data. For the scope of this issue, this is acceptable, but in a real-world application, a `threading.Lock` would be required to protect access to `_next_id` and the `todos` list.
-   **Test State Bleeding**: Without a state-resetting fixture, tests will be order-dependent and flaky. The recommended `pytest` fixture approach is crucial to mitigate this.
-   **Data Persistence**: As this is an in-memory store, all data will be lost when the application restarts. This is by design, as per the issue requirements.
-   **Pydantic Versioning**: The method to convert a model to a dictionary is `dict()` in Pydantic v1 but `model_dump()` in v2. The implementation should use the method appropriate for the version installed in the project's environment. `model_dump()` is recommended for new projects.

## Sources
-   Pydantic Documentation - Field `default_factory`: [https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.Field](https://docs.pydantic.dev/latest/api/fields/#pydantic.fields.Field)
-   Pydantic Documentation - Model Methods (`model_dump`): [https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_dump)
-   Python Documentation - `datetime`: [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
-   Pytest Documentation - Fixtures: [https://docs.pytest.org/en/stable/how-to/fixtures.html](https://docs.pytest.org/en/stable/how-to/fixtures.html)
