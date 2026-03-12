# PLANNING - Issue #1

## Architecture
The solution will introduce a new, self-contained `webapp` component to the project. This component will handle the data layer for a ToDo list application.

1.  **Directory Structure**: A new `webapp` directory will be created at the root level, parallel to the existing `src` directory. This isolates the web application logic from the AI agent orchestration logic. The `webapp` directory will be marked as a Python package by an `__init__.py` file.

2.  **Data Modeling**: A `webapp/models.py` file will define the `Todo` data structure using Pydantic. This provides data validation, type safety, and a single source of truth for the shape of a "todo" item. The model will automatically generate creation timestamps.

3.  **In-Memory Storage**: A `webapp/storage.py` file will implement a simple in-memory database using module-level variables (a list for data and an integer for an ID counter). This module will act as a Data Access Layer, exposing functions (`add_todo`, `list_todos`, `delete_todo`) to manipulate the data. This approach encapsulates the storage logic and prevents direct manipulation of the global state from outside the module.

4.  **Testing**: A new test file, `tests/test_storage.py`, will be created to provide unit tests for the storage layer. It will follow the existing project's testing patterns using `pytest`. A `pytest` fixture will be used to reset the in-memory storage before each test, ensuring test isolation and reliability.

5.  **Dependencies**: The `pydantic` library will be added to `requirements.txt` as a new project dependency.

## Files to Create

### `webapp/__init__.py`
- An empty file to make the `webapp` directory a Python package.

### `webapp/models.py`
- **Imports**: `datetime`, `timezone` from the `datetime` module; `BaseModel`, `Field` from `pydantic`.
- **`Todo` class**: A Pydantic `BaseModel` with the following fields:
    - `id: int`: The unique identifier for the todo.
    - `title: str`: The content of the todo item.
    - `created_at: str`: An ISO 8601 formatted datetime string. It will use `Field(default_factory=...)` to automatically populate with the current UTC time upon creation.

### `webapp/storage.py`
- **Module-level variables**:
    - `todos: list[dict] = []`: An empty list to store the todo dictionaries.
    - `_next_id: int = 1`: An integer to track the next available ID.
- **Functions**:
    - `add_todo(title: str) -> dict`:
        - Creates a `Todo` model instance with the next available ID and the given title.
        - Converts the Pydantic model object to a dictionary.
        - Appends the dictionary to the `todos` list.
        - Increments `_next_id`.
        - Returns the newly created todo dictionary.
    - `list_todos() -> list[dict]`:
        - Returns a copy of the `todos` list.
    - `delete_todo(todo_id: int) -> bool`:
        - Finds and removes the todo dictionary with the matching `todo_id` from the `todos` list.
        - Returns `True` if a todo was found and deleted, `False` otherwise.

### `tests/test_storage.py`
- **Imports**: `pytest`, `webapp.storage`, `re`, `datetime`.
- **`reset_storage` fixture**: A `pytest` fixture using `autouse=True` to clear `webapp.storage.todos` and reset `webapp.storage._next_id` to 1 before each test run.
- **Test functions**:
    - `test_add_todo()`: Verifies that `add_todo` returns a correctly structured dictionary and adds it to the storage list.
    - `test_list_todos()`: Verifies that `list_todos` returns all items that have been added.
    - `test_delete_existing_todo()`: Verifies that `delete_todo` returns `True` and removes the correct item when the ID exists.
    - `test_delete_non_existent_todo()`: Verifies that `delete_todo` returns `False` and does not modify the list when the ID does not exist.
    - `test_ids_auto_increment_correctly()`: Verifies that IDs are unique and increment correctly, even after items have been deleted.

## Files to Modify

### `requirements.txt`
- Add a new line for the `pydantic` dependency: `pydantic`.

## TODO List
1.  **Dependency**: Add `pydantic` to `requirements.txt`. - [simple]
2.  **Packaging**: Create the `webapp` directory and the empty `webapp/__init__.py` file. - [simple]
3.  **Model**: Create `webapp/models.py` and implement the `Todo` Pydantic model. - [simple]
4.  **Storage Setup**: Create `webapp/storage.py` and define the module-level `todos` list and `_next_id` counter. - [simple]
5.  **Storage `add`**: Implement the `add_todo` function in `webapp/storage.py`. - [medium]
6.  **Storage `list`**: Implement the `list_todos` function in `webapp/storage.py`. - [simple]
7.  **Storage `delete`**: Implement the `delete_todo` function in `webapp/storage.py`. - [medium]
8.  **Test Setup**: Create `tests/test_storage.py` and implement the `reset_storage` fixture. - [simple]
9.  **Test `add_todo`**: Write the test case for the `add_todo` function. - [simple]
10. **Test `list_todos`**: Write the test case for the `list_todos` function. - [simple]
11. **Test `delete_todo` (existing)**: Write the test case for deleting an existing todo. - [simple]
12. **Test `delete_todo` (non-existent)**: Write the test case for deleting a non-existent todo. - [simple]
13. **Test ID Incrementation**: Write the test case to verify the ID auto-increment logic after a deletion. - [medium]

## Test Plan
- **`test_add_todo`**:
    - Call `add_todo` with a sample title.
    - Verify the returned value is a dictionary.
    - Verify the dictionary contains the keys `id`, `title`, and `created_at`.
    - Verify `id` is `1` and `title` matches the input.
    - Verify `created_at` is a string matching the ISO 8601 format (e.g., using a regex).
    - Verify the `webapp.storage.todos` list contains one item, which is the returned dictionary.

- **`test_list_todos`**:
    - Call `add_todo` twice with different titles.
    - Call `list_todos`.
    - Verify the returned list contains two dictionaries.
    - Verify the dictionaries match the items that were added.

- **`test_delete_existing_todo`**:
    - Add two todos.
    - Call `delete_todo` with the ID of the first todo (`1`).
    - Verify the function returns `True`.
    - Call `list_todos` and verify it returns a list with only the second todo.

- **`test_delete_non_existent_todo`**:
    - Add one todo.
    - Call `delete_todo` with a non-existent ID (e.g., `99`).
    - Verify the function returns `False`.
    - Call `list_todos` and verify the original todo is still present.

- **`test_ids_auto_increment_correctly`**:
    - Call `add_todo` three times. Verify the IDs are 1, 2, and 3.
    - Call `delete_todo` with ID `2`.
    - Call `add_todo` again.
    - Verify the new todo has an ID of `4`.
    - Call `list_todos` and verify the list contains todos with IDs `1`, `3`, and `4`.
