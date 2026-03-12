# PLANNING - Issue #1

## Architecture
The solution will introduce a new, self-contained Python package named `webapp`. This package will contain the data layer for a ToDo application, completely separate from the existing `src` and `dashboard` logic.

1.  **`webapp/models.py`**: A Pydantic `BaseModel` named `Todo` will be defined here. This model will serve as the single source of truth for the structure and validation of a todo item, including automatic generation of creation timestamps.
2.  **`webapp/storage.py`**: This module will implement an in-memory data store using module-level variables (`list` for todos, `int` for an ID counter). It will expose three functions (`add_todo`, `list_todos`, `delete_todo`) to provide a simple CRUD-like interface. To ensure data consistency, the `add_todo` function will use the `Todo` model from `models.py` to create and validate new items before storing them as plain dictionaries.
3.  **`tests/test_storage.py`**: Unit tests will be created to verify the functionality of `webapp.storage`. A `pytest` fixture will be used to reset the in-memory store before each test, ensuring test isolation and reliability.
4.  **`requirements.txt`**: The `pydantic` library, a new dependency for the `Todo` model, will be added to this file.

This design cleanly encapsulates the new functionality, follows existing project conventions for typing and structure, and establishes a robust testing strategy for the stateful storage module.

## Files to Create
- **`webapp/__init__.py`**
  - An empty file to mark the `webapp` directory as a Python package.
- **`webapp/models.py`**
  - **`Todo` class**: A Pydantic `BaseModel` with fields:
    - `id: int`
    - `title: str`
    - `created_at: str`: Using `Field(default_factory=...)` to automatically generate a UTC datetime string in ISO format.
- **`webapp/storage.py`**
  - **Module-level variables**:
    - `todos: list[dict]`: An empty list to store todo items.
    - `_next_id: int`: A counter for auto-incrementing IDs, starting at 1.
  - **Functions**:
    - `add_todo(title: str) -> dict`: Creates a new todo, adds it to the `todos` list, and returns the created todo dictionary.
    - `list_todos() -> list[dict]`: Returns a copy of the `todos` list.
    - `delete_todo(todo_id: int) -> bool`: Removes a todo by its ID from the list.
- **`tests/test_storage.py`**
  - **`reset_storage` fixture**: A `pytest` fixture with `autouse=True` to clear the `storage.todos` list and reset `storage._next_id` before each test.
  - **Test functions**:
    - `test_add_todo`: Verifies that a new todo is created with the correct structure and data.
    - `test_list_todos`: Verifies that all added todos are returned.
    - `test_delete_todo_success`: Verifies that an existing todo can be deleted and that the function returns `True`.
    - `test_delete_todo_not_found`: Verifies that attempting to delete a non-existent todo returns `False`.
    - `test_id_auto_increments_correctly`: Verifies that IDs increment correctly, even after a deletion.

## Files to Modify
- **`requirements.txt`**
  - Add `pydantic` to the list of dependencies.

## TODO List
1. Create the `webapp` directory. - [simple]
2. Create the empty `webapp/__init__.py` file. - [simple]
3. Add `pydantic` to the `requirements.txt` file. - [simple]
4. Create `webapp/models.py` and implement the `Todo` Pydantic model with `id`, `title`, and an auto-generated `created_at` field. - [medium]
5. Create `webapp/storage.py` and define the module-level `todos` list and `_next_id` counter. - [simple]
6. Implement the `add_todo` function in `webapp/storage.py`, using the `Todo` model for creation and validation. - [medium]
7. Implement the `list_todos` function in `webapp/storage.py`. - [simple]
8. Implement the `delete_todo` function in `webapp/storage.py`. - [medium]
9. Create the test file `tests/test_storage.py`. - [simple]
10. In `tests/test_storage.py`, implement the `reset_storage` `pytest` fixture to ensure test isolation. - [medium]
11. Write the test `test_add_todo` to verify the structure and content of a newly added todo. - [simple]
12. Write the test `test_list_todos` to verify it returns all added items. - [simple]
13. Write the test `test_delete_todo_success` to confirm an existing item is removed and `True` is returned. - [medium]
14. Write the test `test_delete_todo_not_found` to confirm `False` is returned for a non-existent ID. - [simple]
15. Write the test `test_id_auto_increments_correctly` to verify the ID sequence after a deletion. - [medium]

## Test Plan
- **`test_add_todo`**:
  - Call `add_todo("Test Task")`.
  - Verify the returned dictionary has `id=1`, `title="Test Task"`, and a `created_at` key with a valid ISO-formatted timestamp string.
  - Verify that `list_todos()` now contains one item.
- **`test_list_todos`**:
  - Call `add_todo` three times with different titles.
  - Call `list_todos()`.
  - Verify the returned list has a length of 3.
  - Verify the dictionaries in the list match the items that were added.
- **`test_delete_todo_success`**:
  - Add a todo and get its `id`.
  - Call `delete_todo()` with that `id`.
  - Verify the function returns `True`.
  - Call `list_todos()` and verify the list is now empty.
- **`test_delete_todo_not_found`**:
  - Call `delete_todo(999)` on an empty storage.
  - Verify the function returns `False`.
  - Add one todo (which will have `id=1`).
  - Call `delete_todo(999)` again.
  - Verify the function returns `False` and the list still contains one item.
- **`test_id_auto_increments_correctly`**:
  - Add three todos. They should have IDs 1, 2, and 3.
  - Delete the todo with `id=2`.
  - Add a new todo.
  - Verify the new todo has `id=4`.
  - Call `list_todos()` and verify the returned items have IDs 1, 3, and 4.
