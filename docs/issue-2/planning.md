# PLANNING - Issue #2

## Architecture
The proposed solution introduces a new, self-contained `webapp` module to the project, which will house a REST API built with FastAPI. This architecture cleanly separates the new web functionality from the existing AI agent orchestration logic in the `src` directory.

The solution is divided into two main layers within the `webapp` module:
1.  **API Layer (`webapp/api.py`):** This layer is responsible for handling HTTP requests and responses. It will use FastAPI to define endpoints, handle path and body parameters, and manage HTTP status codes and exceptions. It will also include CORS middleware to allow the frontend to communicate with the API.
2.  **Storage Layer (`webapp/storage.py`):** This layer abstracts the data persistence logic. Initially, it will be an in-memory implementation using a Python dictionary, making it simple and dependency-free. The API layer will depend on this storage layer for all CRUD operations, ensuring a clean separation of concerns.

Pydantic models will be used to define the data contracts for request bodies and responses, providing automatic data validation and serialization.

Testing will be done using FastAPI's `TestClient` in a new `tests/test_api.py` file, following the existing `pytest` patterns in the repository. A pytest fixture will be used to ensure the in-memory storage is reset before each test, guaranteeing test isolation.

## Files to Create

### `webapp/__init__.py`
- **Description:** An empty file to mark the `webapp` directory as a Python package, enabling imports like `from webapp.storage import ...`.

### `webapp/storage.py`
- **Description:** Implements the in-memory storage logic for todos. It will be completely decoupled from the FastAPI application itself.
- **Contents:**
    - `_todos`: A `dict` to store todo items, mapping integer IDs to todo dictionaries.
    - `_next_id`: An integer to track the next available ID for a new todo.
    - `get_all_todos() -> list[dict]`: Returns a list of all todo dictionaries.
    - `add_todo(title: str) -> dict`: Creates a new todo, adds it to the storage, and returns the newly created todo dictionary.
    - `delete_todo(todo_id: int) -> dict | None`: Deletes a todo by its ID. Returns the deleted todo if found, otherwise `None`.
    - `_reset_storage()`: A helper function (for testing purposes) to clear the `_todos` dictionary and reset `_next_id`.

### `webapp/api.py`
- **Description:** Contains the main FastAPI application, including routing, request/response models, and endpoint logic.
- **Contents:**
    - **Pydantic Models:**
        - `TodoCreate(BaseModel)`: Defines the shape of the request body for creating a todo (`title: str`).
        - `Todo(BaseModel)`: Defines the shape of a todo object in responses (`id: int`, `title: str`).
    - **FastAPI App:**
        - `app = FastAPI()`: The main application instance.
        - `CORSMiddleware` setup to allow all origins (`*`).
    - **API Endpoints:**
        - `GET /api/todos`: Fetches all todos from `storage.get_all_todos()` and returns them.
        - `POST /api/todos`: Accepts a `TodoCreate` object, calls `storage.add_todo()`, and returns the new `Todo` with a `201 Created` status.
        - `DELETE /api/todos/{todo_id}`: Calls `storage.delete_todo()`. If a todo is deleted, it returns `{"deleted": true}`. If not found, it raises an `HTTPException` with a `404` status.

### `tests/test_api.py`
- **Description:** Contains tests for the FastAPI endpoints using `pytest` and `TestClient`.
- **Contents:**
    - **`client = TestClient(app)`:** An instance of the test client for making requests to the app.
    - **Pytest Fixture:** A fixture that calls `storage._reset_storage()` before each test to ensure a clean state.
    - **Test Functions:**
        - `test_create_todo()`: Tests `POST /api/todos`, checking for a `201` status and the correct JSON response.
        - `test_get_todos()`: Tests `GET /api/todos` by first creating a todo and then verifying its presence in the returned list.
        - `test_delete_existing_todo()`: Tests `DELETE /api/todos/{todo_id}` on a valid ID, checking for a `200` status and `{"deleted": true}` response.
        - `test_delete_non_existent_todo()`: Tests `DELETE /api/todos/{todo_id}` on an invalid ID, checking for a `404` status and the specific error detail message.

## Files to Modify

### `requirements.txt`
- **Description:** The file listing Python project dependencies.
- **Changes:**
    - Add `fastapi` for the web framework.
    - Add `uvicorn[standard]` to provide a performant ASGI server for running the application.

## TODO List
1.  **Create `webapp` directory and add `webapp/__init__.py`** - simple
2.  **Implement the in-memory storage in `webapp/storage.py`** - simple
3.  **Implement the FastAPI application in `webapp/api.py`** - medium
4.  **Add `fastapi` and `uvicorn` to `requirements.txt`** - simple
5.  **Create tests for the API in `tests/test_api.py`** - medium

## Test Plan
The testing will be focused on the API endpoints to ensure they behave as specified. `TestClient` will be used to simulate HTTP requests and assert responses without needing to run a live server. A pytest fixture will ensure the in-memory database is reset between each test case, making tests independent and reliable.

- **POST `/api/todos`:**
    - **Verify:** Send a valid JSON payload `{"title": "Test Todo"}`.
    - **Expect:** a `201 Created` status code and a JSON response body like `{"id": 1, "title": "Test Todo"}`.
- **GET `/api/todos`:**
    - **Verify:** First, create one or more todos using the POST endpoint. Then, send a GET request.
    - **Expect:** a `200 OK` status code and a JSON array response containing the objects of the todos that were created.
- **DELETE `/api/todos/{todo_id}` (Existing):**
    - **Verify:** First, create a todo to get a valid ID (e.g., 1). Then, send a DELETE request to `/api/todos/1`.
    - **Expect:** a `200 OK` status code and a JSON response body of `{"deleted": true}`.
    - **Follow-up:** A subsequent GET request to `/api/todos` should return an empty list.
- **DELETE `/api/todos/{todo_id}` (Non-existent):**
    - **Verify:** Send a DELETE request to an ID that is known not to exist (e.g., `/api/todos/999`).
    - **Expect:** a `404 Not Found` status code and a JSON response body `{"detail": "Todo not found"}`.
