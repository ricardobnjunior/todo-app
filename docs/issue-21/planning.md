# PLANNING - Issue #21

## Architecture
The solution will introduce a new, self-contained `webapp` component to the project. This component will be separate from the existing `src` and `dashboard` applications. It will follow a layered architecture:

1.  **API Layer (`webapp/api.py`)**: This layer will use the FastAPI framework to define and serve the REST API endpoints. It will be responsible for handling HTTP requests, validating incoming data using Pydantic models, handling responses and status codes, and managing CORS settings. It will delegate all data manipulation logic to the Storage Layer.
2.  **Storage Layer (`webapp/storage.py`)**: This layer will act as a data access object (DAO). It will abstract the persistence logic from the API layer. For this implementation, it will provide a simple in-memory storage system using a Python dictionary and an auto-incrementing counter for IDs.

Testing will be implemented in `tests/test_api.py` using FastAPI's `TestClient`, which allows for making in-process requests to the API without needing a live server. This ensures that the API endpoints behave as expected and that the API and storage layers are correctly integrated.

## Files to Create

-   **`webapp/__init__.py`**: An empty file to mark the `webapp` directory as a Python package, allowing for imports like `from webapp.storage import ...`.
-   **`webapp/storage.py`**:
    -   **Description**: This module will implement a simple in-memory storage for ToDo items. It will encapsulate all data manipulation logic.
    -   **Contents**:
        -   In-memory data structures (a dictionary for todos, an integer for ID sequence).
        -   `get_all_todos()`: Returns a list of all todo dictionaries.
        -   `add_todo(title: str)`: Creates a new todo with a unique ID, stores it, and returns it.
        -   `delete_todo(todo_id: int)`: Deletes a todo by its ID. Returns a boolean indicating success.
        -   `reset_storage()`: A helper function to clear the storage, intended for use in tests to ensure isolation.
-   **`webapp/api.py`**:
    -   **Description**: This file will contain the main FastAPI application, including routing, data models, and CORS configuration.
    -   **Contents**:
        -   Pydantic models: `TodoIn` (for creating a todo, `title: str`) and `TodoOut` (for responses, `id: int`, `title: str`).
        -   A `FastAPI` app instance.
        -   `CORSMiddleware` configured to allow all origins (`allow_origins=["*"]`).
        -   Endpoint `GET /api/todos`: Returns a list of all todos.
        -   Endpoint `POST /api/todos`: Accepts a `TodoIn` object, creates a new todo using the storage module, and returns the created `TodoOut` object with a `201 Created` status.
        -   Endpoint `DELETE /api/todos/{todo_id}`: Deletes a todo by its ID. Returns `{"deleted": true}` on success, or raises an `HTTPException` with a `404 Not Found` status if the ID does not exist.
-   **`tests/test_api.py`**:
    -   **Description**: This file will contain functional tests for the FastAPI endpoints.
    -   **Contents**:
        -   `TestClient` instance initialized with the FastAPI `app` from `webapp.api`.
        -   A pytest fixture or setup function that calls `storage.reset_storage()` before each test.
        -   Test functions to verify:
            -   Successful creation of a todo via `POST /api/todos`.
            -   Correct retrieval of todos via `GET /api/todos`.
            -   Successful deletion of a todo via `DELETE /api/todos/{todo_id}`.
            -   Correct `404 Not Found` error when attempting to delete a non-existent todo.

## Files to Modify

-   **`requirements.txt`**:
    -   **Description**: The project's main dependency file.
    -   **Changes**: Add `fastapi`, `uvicorn[standard]`, and `httpx` to support the new web application and its tests.

## TODO List

1.  Create the `webapp/` directory and an empty `webapp/__init__.py` file. - simple
2.  Implement the in-memory storage in `webapp/storage.py` with `get_all_todos`, `add_todo`, `delete_todo`, and `reset_storage` functions. - simple
3.  Define Pydantic models and set up the FastAPI application with CORS middleware in `webapp/api.py`. - medium
4.  Implement the `GET /api/todos` endpoint in `webapp/api.py`. - simple
5.  Implement the `POST /api/todos` endpoint in `webapp/api.py`, ensuring it returns a 201 status code. - medium
6.  Implement the `DELETE /api/todos/{todo_id}` endpoint in `webapp/api.py`, including the 404 error handling. - medium
7.  Add `fastapi`, `uvicorn[standard]`, and `httpx` to `requirements.txt`. - simple
8.  Create `tests/test_api.py` and set up the `TestClient` and a fixture for resetting storage. - medium
9.  Write a test in `tests/test_api.py` to verify the successful creation and retrieval of a todo (`POST` then `GET`). - medium
10. Write a test in `tests/test_api.py` to verify the successful deletion of an existing todo. - simple
11. Write a test in `tests/test_api.py` to verify the 404 error response when deleting a non-existent todo. - simple

## Test Plan

-   **API Endpoint Tests (`tests/test_api.py`)**:
    -   **Test Isolation**: A pytest fixture will be used to call `storage.reset_storage()` before each test function execution. This guarantees that each test runs with a clean in-memory database, preventing state leakage between tests.
    -   **Create Todo**: Send a `POST` request to `/api/todos` with a JSON body `{"title": "Test a todo"}`.
        -   Verify the HTTP status code is `201 Created`.
        -   Verify the JSON response body contains an `id` (integer) and the correct `title`.
    -   **Get Todos**:
        -   First, create a todo using a `POST` request.
        -   Then, send a `GET` request to `/api/todos`.
        -   Verify the status code is `200 OK`.
        -   Verify the response is a JSON array containing the todo that was just created.
    -   **Delete Todo**:
        -   Create a todo via `POST` to get a valid `id`.
        -   Send a `DELETE` request to `/api/todos/{id}` using the obtained ID.
        -   Verify the status code is `200 OK`.
        -   Verify the response body is `{"deleted": true}`.
        -   Send another `GET` request to `/api/todos` and verify the list is now empty.
    -   **Delete Non-existent Todo**:
        -   Send a `DELETE` request to `/api/todos/999` (an ID that is guaranteed not to exist).
        -   Verify the status code is `404 Not Found`.
        -   Verify the response body is `{"detail": "Todo not found"}`.
