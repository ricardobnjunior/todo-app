# PLANNING - Issue #1

## Architecture
The solution introduces a new `webapp` package, distinct from the existing `src` directory, to encapsulate the functionality of a ToDo list application. This architecture is composed of three key components:

1.  **Data Model (`webapp/models.py`)**: A Pydantic `Todo` model will define the data structure, enforce type constraints, and handle automatic generation of creation timestamps. This provides a single source of truth for what a "todo" item looks like.
2.  **In-Memory Storage (`webapp/storage.py`)**: A stateful module that acts as a simple database. It uses module-level variables to store the list of todos (`list[dict]`) and manage an auto-incrementing ID counter. It exposes a simple CRUD-like API (`add_todo`, `list_todos`, `delete_todo`). The storage layer will use the Pydantic model for internal object creation to ensure consistency but will store and return plain dictionaries, decoupling it from the specific model implementation.
3.  **Testing (`tests/test_storage.py`)**: Unit tests will be created to validate the behavior of the storage layer. A critical part of the test architecture will be a `pytest` fixture to reset the in-memory storage before each test, ensuring test isolation and reliability.

This design is modular, testable, and cleanly separates the new application logic from the existing agent orchestration codebase.

## Files to Create
- **`webapp/__init__.py`**: An empty file to define the `webapp` directory as a Python package.
- **`webapp/models.py`**: This file will contain the Pydantic `Todo` data model definition.
  - **`Todo(BaseModel)`**: A Pydantic class with `id: int`, `title: str`, and an automatically generated `created_at: str` field.
- **`webapp/storage.py`**: This file will implement the in-memory storage for todo items.
  - **`todos: list[dict]`**: A module-level list to store todo dictionaries.
  - **`_next_id: int`**: A module-level counter for auto-incrementing IDs.
  - **`add_todo(title: str) -> dict`**: Creates, adds, and returns a new todo.
  - **`list_todos() -> list[dict]`**: Returns a copy of all todos.
  - **`delete_todo(todo_id: int) -> bool`**: Removes a todo by its ID.
- **`tests/test_storage.py`**: This file will contain unit tests for the `webapp.storage` module.
  - **`reset_storage()`**: A `pytest` fixture to ensure a clean state for each test.
  - **Test functions**: `test_add_todo`, `test_list_todos`, `test_delete_existing_todo`, `test_delete_non_existent_todo`, `test_id_auto_increment`.

## Files to Modify
- **`requirements.txt`**: To add the `pydantic` library as a new project dependency.

## TODO List
1. [task] Create the `webapp` directory and the empty `webapp/__init__.py` file. - [simple]
2. [task] Add `pydantic` to the `requirements.txt` file. - [simple]
3. [task] Create `webapp/models.py` and define the `Todo` Pydantic model with `id`, `title`, and auto-generated `created_at` fields. - [simple]
4. [task] Create `webapp/storage.py` and initialize the module-level `todos` list and `_next_id` counter. - [simple]
5. [task] Implement the `add_todo(title: str)` function in `webapp/storage.py`. - [medium]
6. [task] Implement the `list_todos()` function in `webapp/storage.py`, ensuring it returns a copy. - [simple]
7. [task] Implement the `delete_todo(todo_id: int)` function in `webapp/storage.py`. - [medium]
8. [task] Create the `tests/test_storage.py` file and add a `pytest` fixture to reset the storage state before each test. - [medium]
9. [task] Write a test in `tests/test_storage.py` to verify that `add_todo` creates a todo with the correct structure and returns it. - [medium]
10. [task] Write a test in `tests/test_storage.py` to verify that `list_todos` returns all added items. - [simple]
11. [task] Write a test in `tests/test_storage.py` to verify that `delete_todo` returns `True` and removes an existing todo. - [simple]
12. [task] Write a test in `tests/test_storage.py` to verify that `delete_todo` returns `False` for a non-existent todo. - [simple]
13. [task] Write a test in `tests/test_storage.py` to verify that IDs auto-increment correctly after a deletion. - [medium]

## Test Plan
A new test file, `tests/test_storage.py`, will be created to provide comprehensive unit test coverage for the in-memory storage logic.

- **Test Isolation**: A `pytest` fixture with `@pytest.fixture(autouse=True)` will be implemented. This fixture will run before every test function to reset the state of the `webapp.storage` module by clearing the `todos` list and resetting the `_next_id` counter to 1. This is crucial to prevent test results from being influenced by previously run tests.

- **`test_add_todo`**:
  - **It should** add a todo and return the correct dictionary structure.
  - **Verify**: Call `add_todo("My First Task")`, check that the returned dictionary has `id: 1`, `title: "My First Task"`, and that `created_at` is a valid ISO 8601 formatted string. Also verify that `list_todos()` now contains one item.

- **`test_list_todos`**:
  - **It should** return a list of all added todos.
  - **Verify**: Add two or more todos. Call `list_todos()` and assert that the returned list contains the correct number of items with the expected content.

- **`test_delete_todo`**:
  - **It should** return `True` and remove an existing todo.
  - **Verify**: Add a todo, then call `delete_todo()` with its ID. Assert that the function returns `True` and that a subsequent call to `list_todos()` returns an empty list.
  - **It should** return `False` for a non-existent todo.
  - **Verify**: Add a todo with ID 1. Call `delete_todo(99)`. Assert that the function returns `False` and that `list_todos()` still contains the original todo.

- **`test_id_auto_increment`**:
  - **It should** correctly increment IDs even after deletions.
  - **Verify**: Add three todos (getting IDs 1, 2, 3). Delete the todo with ID 2. Add a new todo. Assert that the new todo receives ID 4, and the final list contains todos with IDs 1, 3, and 4.
