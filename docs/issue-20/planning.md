# PLANNING - Issue #20

## Architecture
The proposed solution introduces a new, self-contained `webapp` package for a simple ToDo list application. This package will exist at the top level of the repository, parallel to the existing `src` directory.

The data layer will be split into two components:
1.  **Model (`webapp/models.py`)**: A Pydantic `Todo` model will define the data structure, validation rules, and automatic generation of the `created_at` timestamp. This ensures data consistency.
2.  **Storage (`webapp/storage.py`)**: An in-memory storage module will manage the lifecycle of todo items. It will use module-level variables (`list` for data, `int` for an ID counter) to store state. Functions will be provided for adding, listing, and deleting todos. This layer will work with standard Python dictionaries for data exchange, decoupling it from the Pydantic model implementation by using `model_dump()` for conversion.

Testing will be done using `pytest` in a new `tests/test_storage.py` file. A key part of the test design is a `pytest` fixture that reloads the `webapp.storage` module before each test, guaranteeing test isolation by resetting the in-memory state.

## Files to Create

- **`webapp/__init__.py`**:
  - An empty file to mark the `webapp` directory as a Python package.

- **`webapp/models.py`**:
  - **`class Todo(pydantic.BaseModel)`**: Defines the data model for a todo item.
    - `id: int`
    - `title: str`
    - `created_at: str`: Will use `pydantic.Field` with a `default_factory` to automatically generate a UTC ISO 8601 timestamp string upon instantiation.

- **`webapp/storage.py`**:
  - **`todos: list[dict]`**: A module-level list, initialized as empty, to store the todo items as dictionaries.
  - **`_next_id: int`**: A module-level integer, initialized to `1`, to track the next available ID.
  - **`add_todo(title: str) -> dict`**: Creates a new `Todo` model instance, converts it to a dictionary, appends it to the `todos` list, increments `_next_id`, and returns the dictionary.
  - **`list_todos() -> list[dict]`**: Returns a copy of the `todos` list.
  - **`delete_todo(todo_id: int) -> bool`**: Searches for and removes a todo by its `id`. Returns `True` on success and `False` if not found.

- **`tests/test_storage.py`**:
  - **`reset_storage()`**: A `pytest` fixture that uses `importlib.reload()` on `webapp.storage` to ensure a clean state for each test.
  - **`test_add_todo()`**: Verifies that adding a todo works correctly and returns the right data structure.
  - **`test_list_todos()`**: Verifies that listing returns all added todos.
  - **`test_delete_todo_existing()`**: Verifies that deleting an existing todo works and removes the item.
  - **`test_delete_todo_non_existent()`**: Verifies that attempting to delete a non-existent todo returns `False` and doesn't alter the list.
  - **`test_id_auto_increment()`**: Verifies that IDs increment correctly, even after deletions.

## Files to Modify

- **`requirements.txt`**:
  - Add `pydantic` to the list of project dependencies.

## TODO List

1.  Create the empty `webapp/__init__.py` file. - [simple]
2.  Add `pydantic` as a dependency in `requirements.txt`. - [simple]
3.  Create `webapp/models.py` and implement the `Todo` Pydantic model with an auto-generated `created_at` field. - [medium]
4.  Create `webapp/storage.py` and define the module-level state variables `todos` and `_next_id`. - [simple]
5.  Implement the `add_todo` function in `webapp/storage.py`. - [medium]
6.  Implement the `list_todos` function in `webapp/storage.py`. - [simple]
7.  Implement the `delete_todo` function in `webapp/storage.py`. - [medium]
8.  Create `tests/test_storage.py` and implement the `reset_storage` pytest fixture using `importlib.reload`. - [medium]
9.  Write the test case `test_add_todo` to verify item creation and structure. - [medium]
10. Write the test case `test_list_todos` to verify the full list is returned. - [simple]
11. Write the test case `test_delete_todo_existing` to confirm successful deletion. - [simple]
12. Write the test case `test_delete_todo_non_existent` to confirm correct behavior for non-existent IDs. - [simple]
13. Write the test case `test_id_auto_increment` to verify the ID generation logic after a deletion. - [medium]

## Test Plan

The test plan focuses on unit-testing the `webapp.storage` module's functionality and ensuring its stateful nature is handled correctly during tests.

- **Test Isolation**: A `pytest` fixture using `importlib.reload(webapp.storage)` will be applied to all tests to reset the in-memory database (`todos` list and `_next_id` counter) before each test run. This prevents tests from interfering with each other.

- **`add_todo` Verification**:
  - A test will call `add_todo` and assert that the returned object is a dictionary with the correct `id` (1), `title`, and a valid ISO-formatted `created_at` string.
  - It will also check `list_todos()` to confirm the item was persisted in the in-memory list.

- **`list_todos` Verification**:
  - A test will add multiple todos and then call `list_todos` to assert that the returned list contains the correct number of items and the correct data.

- **`delete_todo` Verification**:
  - **Success Case**: A test will add a todo, then call `delete_todo` with its ID. It will assert that the function returns `True` and that the item is no longer present in `list_todos()`.
  - **Failure Case**: A test will call `delete_todo` with an ID that does not exist and assert that the function returns `False` and that the storage list remains unchanged.

- **ID Auto-Increment Logic**:
  - A dedicated test will perform the following sequence:
    1.  Add three todos and verify their IDs are 1, 2, and 3.
    2.  Delete the todo with ID 2.
    3.  Add a fourth todo.
    4.  Verify that the new todo's ID is 4 (not 2), and the list of IDs in storage is now `[1, 3, 4]`.
