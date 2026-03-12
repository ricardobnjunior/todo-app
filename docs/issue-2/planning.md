# PLANNING - Issue #2

## Architecture
The solution will be implemented by creating a new, self-contained Python package named `webapp`. This package will follow a simple layered architecture:

1.  **API Layer (`api.py`):** Contains the FastAPI application, endpoint definitions (`/api/todos`), request/response handling, and CORS middleware. It will be the main entry point for the REST API.
2.  **Data Models (`models.py`):** Defines the data structures using Pydantic models (`Todo`, `TodoCreate`). This ensures strong data validation and serialization for API requests and responses.
3.  **Storage Layer (`storage.py`):** Provides a simple in-memory data persistence mechanism. It will manage a list of todos and expose functions for creating, retrieving, and deleting them. This layer abstracts the data source from the API layer.

Testing will be handled in a separate `tests/test_api.py` file, utilizing FastAPI's `TestClient` to make requests to the application in a controlled test environment. Test isolation will be guaranteed by resetting the in-memory storage before each test run.

Finally, project dependencies will be updated in `requirements.txt` to include `fastapi` and `uvicorn`.

## Files to Create
- **`webapp/__init__.py`**: An empty file to mark the `webapp` directory as a Python package.
- **`webapp/storage.py`**:
    - Will contain the in-memory data store (a dictionary for todos and an integer sequence for IDs).
    - `get_all_todos()`: Returns a list of all todo items.
    - `add_todo(title: str)`: Creates a new todo, assigns it an ID, adds it to the store, and returns it.
    - `delete_todo(todo_id: int)`: Removes a todo by its ID. Returns the deleted todo object if found, otherwise `None`.
    - `reset_storage()`: A helper function for tests to clear all data and reset the ID sequence.
- **`webapp/models.py`**:
    - Will define Pydantic models for data validation.
    - `TodoCreate(BaseModel)`: A model for the request body of `POST /api/todos`, containing a single `title: str` field.
    - `Todo(BaseModel)`: A model for API responses, containing `id: int` and `title: str` fields.
- **`webapp/api.py`**:
    - The main FastAPI application file.
    - `app = FastAPI()`: The FastAPI application instance.
    - `CORSMiddleware`: Configuration to allow all origins (`*`).
    - `GET /api/todos`: Endpoint to retrieve all todos. It will have a `response_model=list[Todo]`.
    - `POST /api/todos`: Endpoint to create a new todo. It will expect a `TodoCreate` body, use `status_code=201`, and have `response_model=Todo`.
    - `DELETE /api/todos/{todo_id}`: Endpoint to delete a todo by its ID. It will raise `HTTPException(404)` if the todo is not found.
- **`tests/test_api.py`**:
    - Test file for the API endpoints.
    - `from fastapi.testclient import TestClient`: To make requests to the app.
    - A `pytest` fixture that calls `storage.reset_storage()` before each test to ensure isolation.
    - `test_create_and_get_todo()`: Tests `POST` followed by `GET` to verify creation and retrieval.
    - `test_delete_todo()`: Tests `DELETE` on an existing todo and verifies the response.
    - `test_delete_nonexistent_todo()`: Tests `DELETE` on a non-existent todo ID and verifies the `404` response.

## Files to Modify
- **`requirements.txt`**:
    - Add `fastapi` for the web framework.
    - Add `uvicorn[standard]` for the ASGI server.

## TODO List
1. **Create `webapp` package structure**: Create the `webapp` directory and an empty `webapp/__init__.py` file. - [simple]
2. **Implement in-memory storage**: Create `webapp/storage.py` with the data dictionary, ID counter, and functions: `get_all_todos`, `add_todo`, `delete_todo`, and `reset_storage`. - [medium]
3. **Define Pydantic models**: Create `webapp/models.py` with `TodoCreate` and `Todo` BaseModel classes. - [simple]
4. **Implement FastAPI application**: Create `webapp/api.py`, instantiate the FastAPI app, and add the CORS middleware. - [simple]
5. **Implement GET endpoint**: In `webapp/api.py`, create the `GET /api/todos` endpoint that calls `storage.get_all_todos()` and uses the `Todo` response model. - [simple]
6. **Implement POST endpoint**: In `webapp/api.py`, create the `POST /api/todos` endpoint that accepts a `TodoCreate` body, calls `storage.add_todo()`, and returns the created object with a 201 status. - [medium]
7. **Implement DELETE endpoint**: In `webapp/api.py`, create the `DELETE /api/todos/{todo_id}` endpoint that calls `storage.delete_todo()` and handles both success and "not found" cases. - [medium]
8. **Update dependencies**: Add `fastapi` and `uvicorn[standard]` to `requirements.txt`. - [simple]
9. **Create test file and fixture**: Create `tests/test_api.py` and set up the `TestClient` instance. Implement a pytest fixture that automatically resets the storage before each test. - [medium]
10. **Write test for creating a todo**: In `tests/test_api.py`, add a test to `POST` a new todo and verify the 201 status code and the response body. - [simple]
11. **Write test for getting all todos**: In `tests/test_api.py`, extend the creation test or add a new one to `GET /api/todos` and verify the list contains the newly created todo. - [simple]
12. **Write test for deleting a todo**: In `tests/test_api.py`, add a test to create a todo, then delete it, verifying the 200 status code and `{"deleted": true}` response. - [simple]
13. **Write test for deleting a non-existent todo**: In `tests/test_api.py`, add a test to attempt deleting an invalid ID and verify the 404 status code and error detail. - [simple]

## Test Plan
- **Unit/Integration Tests**: The tests will live in `tests/test_api.py` and will be executed by `pytest`.
- **Test Environment**: FastAPI's `TestClient` will be used to make HTTP requests directly to the application without needing a live server. This provides fast and reliable integration testing of the API layer.
- **State Management**: A pytest fixture will be used to call a `storage.reset_storage()` function before each test. This ensures that the in-memory database is empty and tests are independent and deterministic.
- **Test Cases**:
    - **Create**: Send a `POST` request to `/api/todos` with a valid JSON body. Verify the status code is `201 Created` and the JSON response contains the correct `title` and a new `id`.
    - **Read**: After creating a todo, send a `GET` request to `/api/todos`. Verify the status code is `200 OK` and the response is a JSON array containing the todo that was just created.
    - **Delete (Success)**: Create a todo, get its `id`, then send a `DELETE` request to `/api/todos/{id}`. Verify the status code is `200 OK` and the response body is `{"deleted": true}`.
    - **Delete (Not Found)**: Send a `DELETE` request to `/api/todos/999` (an ID that does not exist). Verify the status code is `404 Not Found` and the response body contains the specified detail message.
