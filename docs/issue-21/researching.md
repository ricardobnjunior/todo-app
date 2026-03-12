# RESEARCHING - Issue #21

## Research Findings
### FastAPI for REST APIs
FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.

-   **Path Operations**: Endpoints are defined using decorators (`@app.get`, `@app.post`, `@app.delete`, etc.) on top of standard Python functions.
-   **Data Validation and Serialization**: FastAPI uses Pydantic models to define data schemas. It automatically handles request validation, data conversion, and response serialization based on these models. This is ideal for the `{"title": "..."}` request body and the structured JSON responses.
-   **Path Parameters**: To capture parts of the URL path, like `todo_id` in `/api/todos/{todo_id}`, you declare them as function arguments with type hints (e.g., `def delete_todo(todo_id: int):`). FastAPI handles parsing and type validation.
-   **Status Codes**: By default, `POST` operations return `200 OK`. To return `201 Created` as requested, the `status_code` argument can be set in the decorator: `@app.post("/api/todos", status_code=201)`.
-   **Error Handling**: To return specific HTTP error codes like `404 Not Found`, the recommended practice is to raise an `HTTPException` from `fastapi`. This will interrupt the request and send the appropriate HTTP response.
-   **CORS (Cross-Origin Resource Sharing)**: FastAPI provides a `CORSMiddleware` to handle requests from different origins (e.g., a frontend running on a different domain or port). It can be configured to allow all origins, methods, and headers, as specified in the issue. The configuration `allow_origins=["*"]` is used for this.

### Testing FastAPI Applications
The framework provides a `TestClient` for testing API endpoints.

-   `TestClient` is built on top of `httpx`.
-   It allows you to make requests to the FastAPI application directly without needing a running server.
-   You instantiate the client by passing the FastAPI app instance: `client = TestClient(app)`.
-   Standard methods like `client.get()`, `client.post()`, etc., are used to interact with the endpoints.
-   The response object contains the `status_code`, `json()` method to parse the body, and other details needed for assertions.

### Storage Abstraction
The issue mentions separating the API logic from the data storage layer by using a `webapp.storage` module. For a simple application like this, an in-memory data structure (e.g., a dictionary) within the `storage` module is a common and effective pattern. This isolates persistence logic and makes the API layer more testable and easier to modify if the storage mechanism changes later (e.g., to a database). The storage module would typically export functions like `add_todo`, `delete_todo`, and `get_all_todos`.

## Duplication Check
The existing codebase is focused on an AI agent orchestration system that interacts with GitHub repositories. The main application logic resides in `src/`, with another separate application in `dashboard/`.

-   **No FastAPI Usage**: There is no existing usage of FastAPI or any other web framework for building a REST API within the repository. The task requires creating an entirely new, self-contained `webapp` module.
-   **No API Tests**: Consequently, there are no existing tests for REST APIs. The current tests in `tests/` use `unittest.mock` and `pytest` for unit and integration testing of the agent logic. While there's no code to reuse, the testing pattern of using `pytest` and creating helper functions is a good convention to follow.
-   **No Pydantic Models**: The project does not currently use Pydantic for data modeling. This will be a new dependency and pattern introduced for the `webapp`.

Conclusion: The required functionality is entirely new. There is no existing code that can be reused or refactored. The implementation will be from scratch.

## Recommended Approach
1.  **Create `webapp/storage.py`**:
    *   Implement a simple in-memory storage using a global dictionary to hold todos and a counter for auto-incrementing IDs.
    *   Expose functions: `get_all_todos()`, `add_todo(title: str)`, and `delete_todo(todo_id: int)`. The `delete_todo` function should return a boolean indicating success or failure (if the ID wasn't found). A `reset_storage()` function should also be added to facilitate test isolation.

2.  **Create `webapp/api.py`**:
    *   Define Pydantic models: `TodoIn` (for `POST` request body with `title: str`) and `TodoOut` (for responses with `id: int` and `title: str`).
    *   Instantiate a `FastAPI` application.
    *   Add `CORSMiddleware` to the app, configured with `allow_origins=["*"]`, `allow_credentials=True`, `allow_methods=["*"]`, and `allow_headers=["*"]`.
    *   Implement the three required endpoints, importing and using the functions from `webapp.storage`.
        *   `GET /api/todos`: Call `storage.get_all_todos()` and set `response_model=list[TodoOut]`.
        *   `POST /api/todos`: Accept a `TodoIn` object, call `storage.add_todo()`, and return the result with `status_code=201` and `response_model=TodoOut`.
        *   `DELETE /api/todos/{todo_id}`: Call `storage.delete_todo()`. If it returns `False`, raise `HTTPException(status_code=404, detail="Todo not found")`. If `True`, return `{"deleted": true}`.

3.  **Create `tests/test_api.py`**:
    *   Import `TestClient` and the `app` object from `webapp.api`.
    *   Use a pytest fixture or a simple setup/teardown function to call `storage.reset_storage()` before tests to ensure a clean state.
    *   Create `TestClient(app)`.
    *   Write test functions to cover the requirements:
        *   Test `POST` creates a todo and returns 201 with the correct data.
        *   Test `GET` retrieves a list containing the newly created todo.
        *   Test `DELETE` on an existing ID returns 200 and `{"deleted": true}`.
        *   Test `DELETE` on a non-existent ID returns 404.

4.  **Update `requirements.txt`**:
    *   Add `fastapi`, `uvicorn[standard]`, and `httpx` to the project's root `requirements.txt`.

This approach aligns with FastAPI best practices, fulfills all issue requirements, and modularizes the application by separating API logic from storage.

## Risks and Edge Cases
-   **Storage Thread Safety**: The recommended in-memory storage (a global Python dictionary) is not thread-safe. If the application is run with multiple worker processes, race conditions could occur when modifying the dictionary (e.g., two simultaneous `POST` requests). For the scope of this task, this is an acceptable simplification.
-   **Test State Management**: The required tests (create, then read, then delete) create a dependency between test steps. A single test function covering the whole workflow is simple, but can be brittle. A better, more robust pattern would be to use pytest fixtures to ensure each test function runs independently, but this adds complexity that may not be necessary for this task.
-   **CORS Security**: Allowing all origins (`"*"`) is convenient for development but is insecure for production environments. The implementation should match the requirement, but it's a known-risk configuration.
-   **ID Collision**: Using a simple integer counter for IDs in an in-memory store means IDs will reset every time the server restarts. This is fine for this exercise but would be unsuitable for a real application requiring persistence.
-   **Input Validation of `todo_id`**: The `DELETE` endpoint expects an integer ID. If a non-integer string is provided (e.g., `/api/todos/abc`), FastAPI's built-in validation will automatically respond with a `422 Unprocessable Entity` error, which is the correct behavior and does not require custom handling.

## Sources
-   FastAPI Documentation - First Steps: [https://fastapi.tiangolo.com/tutorial/first-steps/](https://fastapi.tiangolo.com/tutorial/first-steps/)
-   FastAPI Documentation - Path Parameters: [https://fastapi.tiangolo.com/tutorial/path-params/](https://fastapi.tiangolo.com/tutorial/path-params/)
-   FastAPI Documentation - Request Body (Pydantic): [https://fastapi.tiangolo.com/tutorial/body/](https://fastapi.tiangolo.com/tutorial/body/)
-   FastAPI Documentation - Handling Errors: [https://fastapi.tiangolo.com/tutorial/handling-errors/](https://fastapi.tiangolo.com/tutorial/handling-errors/)
-   FastAPI Documentation - CORS (Cross-Origin Resource Sharing): [https://fastapi.tiangolo.com/tutorial/cors/](https://fastapi.tiangolo.com/tutorial/cors/)
-   FastAPI Documentation - Testing: [https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)
