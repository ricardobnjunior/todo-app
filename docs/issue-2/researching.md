# RESEARCHING - Issue #2

## Research Findings
### FastAPI Best Practices
FastAPI is a modern web framework for Python that uses standard Python type hints. Best practices for creating a simple CRUD API include:
1.  **Pydantic Models**: Use Pydantic models to define the data shape for request bodies and responses. This gives you data validation, serialization, and automatic documentation generation. For this task, we'll need a model for creating a todo (e.g., `TodoCreate`) which only has a `title`, and a model for representing a stored todo (e.g., `Todo`) which has an `id` and a `title`.
2.  **Path Operations**: Use decorators (`@app.get`, `@app.post`, etc.) to define API endpoints.
    - For `POST` creating a resource, it's standard practice to return a `201 Created` status code. This can be done by setting `status_code=201` in the decorator.
    - For `GET` operations returning a list, FastAPI automatically handles serializing a list of Pydantic models to a JSON array. Specifying `response_model=list[Todo]` ensures the output format is correct and documented.
    - For operations on a specific item like `DELETE /api/todos/{todo_id}`, use path parameters (`{todo_id}`) to identify the resource.
3.  **Error Handling**: To return HTTP error responses like 404 Not Found, the standard approach is to raise `fastapi.HTTPException`. This allows you to specify the status code and a detail message, which FastAPI converts into the correct JSON error response.
4.  **Middleware**: FastAPI has a simple system for adding middleware. For enabling Cross-Origin Resource Sharing (CORS), the framework provides `CORSMiddleware`. As requested, it can be configured to allow all origins (`allow_origins=["*"]`).
5.  **Testing**: FastAPI provides a `TestClient` that allows you to make requests to your application in tests without needing a running server. The `TestClient` offers an interface that mimics the `requests` library, making it intuitive to use.

### Storage Layer Decoupling
The issue correctly specifies separating the API logic from the storage logic by placing storage functions in `webapp/storage.py`. This is a crucial design pattern. The API endpoints should be concerned with handling HTTP requests and responses, while the storage module handles the business logic of how and where data is stored (in this case, in-memory). This makes the code easier to test and maintain, and allows for swapping the storage backend (e.g., to a database) in the future without changing the API layer.

## Duplication Check
The codebase does not contain any existing REST API servers built with FastAPI.
- `dashboard/app.py` is not a web server. It's a script that uses the `pygithub` library client-side to fetch data from the GitHub API and generate a report or data structure. It does not define any HTTP endpoints.
- The `src/` directory contains business logic for an AI agent orchestration system. Files like `github_client.py` act as clients to an external API (GitHub), which is the reverse of what this issue requires (building a server).
- The testing framework in `tests/` uses `pytest` and `unittest.mock`. The new tests in `tests/test_api.py` should follow this established pattern, but no existing test code for a web API can be reused.

Given the lack of existing server-side API code, the implementation for this issue will be entirely new. No refactoring or extension of existing code is possible.

## Recommended Approach
1.  **Create `webapp/storage.py`**:
    - Implement a simple in-memory storage using a Python dictionary to hold todos and a counter for generating new IDs.
    - Expose the following functions:
        - `get_all_todos() -> list[dict]`: Returns all todos.
        - `add_todo(title: str) -> dict`: Creates a new todo, adds it to the dictionary, and returns the new todo object.
        - `delete_todo(todo_id: int) -> dict | None`: Removes a todo by its ID. Returns the deleted todo if found, otherwise returns `None`.

2.  **Create `webapp/api.py`**:
    - Import `FastAPI`, `HTTPException`, and `CORSMiddleware`.
    - Import the functions from `webapp.storage`.
    - Define Pydantic models: `TodoCreate(BaseModel)` with `title: str`, and `Todo(BaseModel)` with `id: int` and `title: str`.
    - Initialize the FastAPI app: `app = FastAPI()`.
    - Add the `CORSMiddleware`, configured to allow all origins, methods, and headers.
    - Implement the three required endpoints, using the storage functions and appropriate Pydantic models for request bodies and response models.
        - `GET /api/todos`: Use `response_model=list[Todo]`.
        - `POST /api/todos`: Use `status_code=201`, accept `TodoCreate` as the body, and use `response_model=Todo`.
        - `DELETE /api/todos/{todo_id}`: If `storage.delete_todo` returns `None`, raise `HTTPException(status_code=404, detail="Todo not found")`. Otherwise, return `{"deleted": true}`.

3.  **Create `tests/test_api.py`**:
    - Import `TestClient` from `fastapi.testclient` and the `app` instance from `webapp.api.py`.
    - Instantiate the client: `client = TestClient(app)`.
    - Write tests to cover the required scenarios:
        - A test for creating a new todo (`POST /api/todos`), verifying the `201` status and the response body.
        - A test for listing todos (`GET /api/todos`) that checks if the previously created todo is present.
        - A test for deleting an existing todo (`DELETE /api/todos/{todo_id}`), verifying the `200` status and the `{"deleted": true}` response.
        - A test for deleting a non-existent todo, verifying the `404` status code and error detail.
    - **Note:** It is important to manage state between tests. Using a pytest fixture to reset the in-memory storage before each test run is the cleanest approach.

4.  **Update `requirements.txt`**: Add `fastapi` and `uvicorn` to the file.

## Risks and Edge Cases
- **In-Memory Storage**: The state is volatile and will be lost on application restart. This is acceptable for the scope of the current issue but is not suitable for a production application.
- **Concurrency**: The simple in-memory storage (e.g., a global dictionary and counter) is not thread-safe. In a multi-threaded ASGI server environment, simultaneous requests could lead to race conditions (e.g., two requests getting the same ID). While unlikely to be an issue for this exercise, in a real-world scenario, a `threading.Lock` would be needed to protect write operations.
- **Input Validation**: The requirement `{"title": "..."}` is ambiguous about empty titles. Pydantic will accept `{"title": ""}`. If empty titles should be disallowed, a `Field` validator from Pydantic (`Field(min_length=1)`) should be used in the `TodoCreate` model.
- **ID Type**: Using an integer for `todo_id` is fine for this example, but it should be noted that in the path operation `@app.delete("/api/todos/{todo_id}")`, `todo_id` will be a string. FastAPI handles the conversion to `int` if the type hint is `todo_id: int`, but invalid input (e.g., a non-integer string) will correctly result in a `422 Unprocessable Entity` response, which is a desirable behavior.

## Sources
- FastAPI Documentation - Tutorial - User Guide: [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/)
- FastAPI Documentation - Handling Errors: [https://fastapi.tiangolo.com/tutorial/handling-errors/](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- FastAPI Documentation - CORS (Cross-Origin Resource Sharing): [https://fastapi.tiangolo.com/tutorial/cors/](https://fastapi.tiangolo.com/tutorial/cors/)
- FastAPI Documentation - Testing: [https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)
- Pydantic Documentation: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
