# PLANNING - Issue #1

## Architecture
The proposed solution introduces a new `webapp` package at the root of the project to encapsulate the application's core logic, distinct from the existing `src` (agent tooling) and `dashboard` (monitoring) directories.

The `webapp` package will contain two modules:
1.  **`models.py`**: This module will define the data schema using a Pydantic `BaseModel`. The `Todo` model will serve as the single source of truth for the structure of a todo item, including data types and automatic field generation (`created_at`).
2.  **`storage.py`**: This module will implement a simple, non-persistent, in-memory storage layer. It will use module-level variables (a list for data and an integer for an ID counter) to store todo items as dictionaries. This module will provide functions to add, list, and delete todos. It will operate on simple `dict` objects to remain decoupled from Pydantic models at runtime, adhering to the issue's requirements.

Testing will be done in a new file, `tests/test_storage.py`, using `pytest`. A key part of the test design is a `pytest` fixture to reset the in-memory storage state before each test, ensuring test isolation.

Finally, `pydantic` will be added as a project dependency in `requirements.txt`.

## Files to Create

1.  **`webapp/__init__.py`**
    - **Description:** An empty file to make the `webapp` directory a Python package.

2.  **`webapp/models.py`**
    - **Description:** Contains the Pydantic data model for a `Todo` item.
    - **Contents:**
        - `Todo` (class): A Pydantic `BaseModel` with fields `id` (int), `title` (str), and `created_at` (str). The `created_at` field will use `Field(default_factory=...)` to automatically generate a timezone-aware ISO 8601 datetime string.

3.  **`webapp/storage.py`**
    - **Description:** Implements the in-memory storage logic for todo items.
    - **Contents:**
        - `todos` (module-level `list[dict]`): Stores the todo items. Initialized as an empty list.
        - `_next_id` (module-level `int`): A counter for auto-incrementing todo IDs. Initialized to `1`.
        - `add_todo(title: str) -> dict`: Creates a new todo dict, appends it to `todos`, increments `_next_id`, and returns the created todo.
        - `list_todos() -> list[dict]`: Returns a copy of the `todos` list.
        - `delete_todo(todo_id: int) -> bool`: Removes a todo from the `todos` list by its ID. Returns `True` on success, `False` if not found.

4.  **`tests/test_storage.py`**
    - **Description:** Contains unit tests for the `webapp.storage` module.
    - **Contents:**
        - A `pytest` fixture with `autouse=True` to reset the state of `webapp.storage` before each test.
        - Test functions to cover adding, listing, and deleting todos, as well as verifying ID auto-increment logic.

## Files to Modify

1.  **`requirements.txt`**
    - **Description:** Add the `pydantic` library as a new dependency.

## TODO List

1.  Create the `webapp` directory. - [simple]
2.  Create the empty `webapp/__init__.py` file. - [simple]
3.  Create `webapp/models.py` and define the `Todo` Pydantic model with `id`, `title`, and auto-generated `created_at`. - [simple]
4.  Create `webapp/storage.py` with the module-level `todos` list and `_next_id` counter. - [simple]
5.  Implement the `add_todo` function in `webapp/storage.py`. - [simple]
6.  Implement the `list_todos` function in `webapp/storage.py`. - [simple]
7.  Implement the `delete_todo` function in `webapp/storage.py`. - [medium]
8.  Create the test file `tests/test_storage.py`. - [simple]
9.  In `tests/test_storage.py`, implement the `pytest` fixture to reset storage state before each test. - [medium]
10. In `tests/test_storage.py`, write a test for `add_todo` verifying the return value and side effect. - [simple]
11. In `tests/test_storage.py`, write a test for `list_todos` to ensure it returns all added items. - [simple]
12. In `tests/test_storage.py`, write a test for `delete_todo` with an existing ID, verifying it returns `True` and removes the item. - [simple]
13. In `tests/test_storage.py`, write a test for `delete_todo` with a non-existent ID, verifying it returns `False`. - [simple]
14. In `tests/test_storage.py`, write a test to verify that IDs auto-increment correctly after a deletion. - [medium]
15. Add `pydantic` to the `requirements.txt` file. - [simple]

## Test Plan

The tests will be located in `tests/test_storage.py` and will validate the functionality of the in-memory storage layer. A `pytest` fixture will reset the storage state before each test to ensure they are independent and deterministic.

**Test Cases:**

1.  **`test_add_todo`**:
    - **Verify**: Calling `add_todo("Test task")` returns a dictionary with an `id` of `1`, the correct `title`, and a valid ISO-formatted `created_at` string.
    - **Verify**: After the call, `list_todos()` returns a list containing the newly created task.

2.  **`test_list_todos`**:
    - **Setup**: Add two or three todos.
    - **Verify**: Calling `list_todos()` returns a list with a length equal to the number of todos added.
    - **Verify**: The contents of the list match the todos that were added.

3.  **`test_delete_existing_todo`**:
    - **Setup**: Add a todo.
    - **Verify**: Calling `delete_todo()` with the `id` of the added todo returns `True`.
    - **Verify**: A subsequent call to `list_todos()` returns an empty list.

4.  **`test_delete_non_existent_todo`**:
    - **Setup**: Add one todo (e.g., with ID 1).
    - **Verify**: Calling `delete_todo()` with a non-existent `id` (e.g., `99`) returns `False`.
    - **Verify**: `list_todos()` still contains the original todo.

5.  **`test_id_auto_increment`**:
    - **Setup**:
        1. Add three todos (they should get IDs 1, 2, 3).
        2. Delete the todo with ID 2.
    - **Action**: Add a new todo.
    - **Verify**: The newly added todo has an `id` of `4`.
    - **Verify**: `list_todos()` now contains todos with IDs 1, 3, and 4.
