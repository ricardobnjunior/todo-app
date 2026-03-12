# PLANNING - Issue #1

## Architecture
The solution introduces a new, self-contained `webapp` package to manage ToDo list data. The architecture is composed of three main parts:
1.  **Data Model (`webapp/models.py`)**: A Pydantic `Todo` model will define the data structure, ensuring type safety and providing automatic timestamp generation. This separates the definition of a "todo" from its storage.
2.  **In-Memory Storage (`webapp/storage.py`)**: A module that acts as a simple Data Access Layer (DAL). It uses module-level variables (`list` and `int`) to store the todo items and manage unique IDs. It exposes functions for adding, listing, and deleting todos, encapsulating the state management logic.
3.  **Testing (`tests/test_storage.py`)**: Unit tests using `pytest` will validate the functionality of the storage layer. A `pytest` fixture will be used to reset the in-memory state before each test, ensuring test isolation and reliability.

This design is simple, modular, and directly addresses the requirements while following established best practices seen in the repository, such as clear separation of concerns, type hinting, and comprehensive testing.

## Files to Create

-   **`webapp/__init__.py`**
    -   An empty file to mark the `webapp` directory as a Python package.

-   **`webapp/models.py`**
    -   Will contain the Pydantic `Todo` model.
    -   **`class Todo(BaseModel)`**:
        -   `id: int`
        -   `title: str`
        -   `created_at: str`: with a `default_factory` to automatically generate an ISO 8601 formatted timestamp in UTC.

-   **`webapp/storage.py`**
    -   Will implement the in-memory storage logic for todos.
    -   Module-level variables:
        -   `todos: list[dict] = []`
        -   `_next_id: int = 1`
    -   **`add_todo(title: str) -> dict`**: Creates a new todo, adds it to the `todos` list, and returns it as a dictionary.
    -   **`list_todos() -> list[dict]`**: Returns a copy of the `todos` list.
    -   **`delete_todo(todo_id: int) -> bool`**: Removes a todo by its ID from the list.

-   **`tests/test_storage.py`**
    -   Will contain `pytest` unit tests for the functions in `webapp.storage`.
    -   A `pytest` fixture will be defined to reset the storage state before each test run.
    -   Test functions will cover adding, listing, deleting existing/non-existing todos, and the auto-incrementing ID logic.

## Files to Modify

-   **`requirements.txt`**
    -   Add `pydantic` to the list of project dependencies.

## TODO List
1. Create the `webapp` directory and an empty `webapp/__init__.py` file. - simple
2. Add `pydantic` to the `requirements.txt` file. - simple
3. In `webapp/models.py`, define the `Todo` Pydantic model with `id`, `title`, and auto-generated `created_at` fields. - simple
4. In `webapp/storage.py`, initialize the `todos` list and `_next_id` counter. - simple
5. In `webapp/storage.py`, implement the `add_todo(title: str) -> dict` function. - medium
6. In `webapp/storage.py`, implement the `list_todos() -> list[dict]` function. - simple
7. In `webapp/storage.py`, implement the `delete_todo(todo_id: int) -> bool` function. - medium
8. Create `tests/test_storage.py` and add a `pytest` fixture to reset the storage state before each test. - medium
9. In `tests/test_storage.py`, write a test for `add_todo` to verify the returned structure and that the item is added to storage. - simple
10. In `tests/test_storage.py`, write a test for `list_todos` to ensure it returns all added items. - simple
11. In `tests/test_storage.py`, write a test for `delete_todo` with an existing ID, verifying it returns `True` and the item is removed. - simple
12. In `tests/test_storage.py`, write a test for `delete_todo` with a non-existent ID, verifying it returns `False`. - simple
13. In `tests/test_storage.py`, write a dedicated test to verify that IDs auto-increment correctly after a deletion. - medium

## Test Plan
The test plan focuses on validating the correctness and isolation of the in-memory storage operations.

-   **Test `add_todo`**:
    -   **Verify**: Calling `add_todo` returns a dictionary with the correct `id`, `title`, and a valid ISO-formatted `created_at` string.
    -   **Verify**: The global `todos` list in `webapp.storage` contains the newly created todo.

-   **Test `list_todos`**:
    -   **Verify**: Calling `list_todos` on a fresh state returns an empty list.
    -   **Verify**: After adding multiple todos, `list_todos` returns a list containing all the added items.

-   **Test `delete_todo`**:
    -   **Verify**: Calling `delete_todo` with the ID of an existing item returns `True`.
    -   **Verify**: After a successful deletion, `list_todos` returns a list that no longer contains the deleted item.
    -   **Verify**: Calling `delete_todo` with an ID that does not exist returns `False`.
    -   **Verify**: After a failed deletion attempt, the `todos` list remains unchanged.

-   **Test ID Auto-increment Logic**:
    -   **Verify**: Adding several items results in sequential IDs (1, 2, 3).
    -   **Verify**: After deleting an item from the middle (e.g., ID 2), adding a new item results in a new, non-recycled ID (e.g., 4). The resulting list of IDs should be `[1, 3, 4]`.

-   **Test State Isolation**:
    -   **Verify**: The `pytest` fixture correctly resets the `todos` list and `_next_id` counter before each test, ensuring no state "leaks" between tests.
