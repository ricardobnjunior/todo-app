# RESEARCHING - Issue #2

## Research Findings
Based on the issue description, the primary library to research is **FastAPI**.

1.  **FastAPI Application and Routing:**
    *   An application is created by instantiating `app = FastAPI()`.
    *   Routes are defined using decorators: `@app.get("/path")`, `@app.post("/path")`, `@app.delete("/path")`.
    *   Path parameters are defined in the URL string (e.g., `/todos/{todo_id}`) and passed as function arguments with type hints (e.g., `todo_id: int`). FastAPI automatically handles type validation and conversion.
    *   Returning a dictionary, list, or Pydantic model will automatically be converted to a JSON response.

2.  **Request Body and Data Validation:**
    *   FastAPI uses **Pydantic** models to define the structure and data types of request bodies. For the `POST /api/todos` endpoint, a model like `class TodoCreate(BaseModel): title: str` is the best practice. This provides automatic data validation, conversion, and documentation.
    *   Similarly, a `Todo(BaseModel): id: int; title: str` model should be used to define the response structure for GET and POST endpoints, ensuring consistent output. This is specified via the `response_model` argument in the decorator.

3.  **Status Codes and Error Handling:**
    *   By default, FastAPI returns a `200 OK` status. For successful creation (`POST`), a `201 Created` is more appropriate and can be set using `status_code=201` or `status_code=status.HTTP_201_CREATED` in the decorator.
    *   For "not found" errors, the standard practice is to raise an `HTTPException` from `fastapi`. Example: `raise HTTPException(status_code=404, detail="Todo not found")`. This automatically generates the correct HTTP response.

4.  **CORS (Cross-Origin Resource Sharing):**
    *   FastAPI provides `CORSMiddleware` to handle CORS.
    *   It's added to the application using `app.add_middleware()`.
    *   To allow all origins, as requested, the configuration is `allow_origins=["*"]`. It's also best practice to allow all methods and headers for a permissive development setup: `allow_methods=["*"]`, `allow_headers=["*"]`.

5.  **Testing:**
    *   FastAPI's documentation strongly recommends using its `TestClient`.
    *   The `TestClient` is a wrapper around `httpx` and provides a simple way to make requests to the app within a test suite.
    *   It is instantiated with the app object: `client = TestClient(app)`.
    *   Requests are made via methods like `client.get()`, `client.post()`, `client.delete()`.
    *   The response object allows for assertions on `response.status_code` and `response.json()`.
    *   To ensure tests are isolated, any underlying state (like an in-memory database) should be reset before each test. A pytest fixture is the ideal mechanism for this.

## Duplication Check
The repository does not contain any existing FastAPI applications or REST API endpoints.

*   `dashboard/app.py` is a dashboard application (likely Streamlit or Dash) and not a REST API server.
*   The code in `src/` is focused on the AI agent's logic and its interaction with the GitHub API as a client.
*   The `tests/` directory contains tests for the existing agent logic, primarily using `pytest` and `unittest.mock.patch`.

There is no code to reuse or refactor for creating the REST API. This will be a net-new addition to the project, correctly isolated within a new `webapp` directory as specified in the issue. The existing testing patterns with `pytest` are a good guide, but the specific implementation will use `TestClient` as per FastAPI best practices.

## Recommended Approach
1.  **Create a `webapp` Package:** Create a new directory `webapp/` with an empty `webapp/__init__.py` to make it a Python package.

2.  **Implement In-Memory Storage:** Create `webapp/storage.py`. Since no database is specified, implement a simple in-memory storage using a module-level dictionary and an integer for ID sequencing. This module should expose `get_all_todos()`, `add_todo(title)`, and `delete_todo(todo_id)`. The delete function should return the deleted object on success and `None` on failure, allowing the API layer to determine if a 404 is needed.

3.  **Define Pydantic Models:** Create `webapp/models.py` to define the data shapes:
    *   `TodoCreate(BaseModel)` with a required `title: str`.
    *   `Todo(BaseModel)` with `id: int` and `title: str`.

4.  **Build the API:** Create `webapp/api.py`:
    *   Import `FastAPI`, `HTTPException`, `status`, and `CORSMiddleware`.
    *   Import the functions from `webapp.storage` and models from `webapp.models`.
    *   Instantiate `app = FastAPI()`.
    *   Add the `CORSMiddleware` with `allow_origins=["*"]`, `allow_methods=["*"]`, and `allow_headers=["*"]`.
    *   Implement the `GET /api/todos` endpoint, using `response_model=list[Todo]`.
    *   Implement the `POST /api/todos` endpoint, accepting a `TodoCreate` body, setting `status_code=status.HTTP_201_CREATED`, and using `response_model=Todo`.
    *   Implement the `DELETE /api/todos/{todo_id}` endpoint. Call the storage function and return `{"deleted": true}` on success or raise a 404 `HTTPException` if the storage function returns `None`.

5.  **Write Tests:** Create `tests/test_api.py`:
    *   Import `TestClient` from `fastapi.testclient` and the `app` instance from `webapp.api`.
    *   Import the `storage` module from `webapp`.
    *   Create a pytest fixture or a setup/teardown function that clears the in-memory storage before each test to ensure test isolation.
    *   Write separate test functions for each scenario outlined in the issue: creating a todo, getting the list, deleting an existing todo, and attempting to delete a non-existent todo. Use the `TestClient` to make requests and `assert` the status codes and JSON responses.

6.  **Update Dependencies:** Add `fastapi` and `uvicorn` to the `requirements.txt` file.

## Risks and Edge Cases
*   **Missing Storage Dependency:** The issue requires using `webapp.storage`, which does not exist. This plan mitigates the risk by proposing a simple in-memory implementation, which is sufficient for this task.
*   **Test State Leakage:** If the in-memory storage is not reset between tests, tests will become dependent on each other and produce non-deterministic results. Using a pytest fixture to reset the state is crucial.
*   **Concurrency:** A simple module-level dictionary is not thread-safe. For a real application, this would be a significant issue, but for this exercise, where requests are likely handled sequentially by `uvicorn`'s default workers (or in tests), it is an acceptable simplification.
*   **Data Validation:** While Pydantic handles type validation, it will not, by default, prevent empty strings (`""`) for a title. This is a minor edge case that can be ignored for now but would require a `Field` validator in Pydantic for a more robust implementation.

## Sources
*   **FastAPI Tutorial:** [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/)
*   **Path Parameters:** [https://fastapi.tiangolo.com/tutorial/path-params/](https://fastapi.tiangolo.com/tutorial/path-params/)
*   **Request Body:** [https://fastapi.tiangolo.com/tutorial/body/](https://fastapi.tiangolo.com/tutorial/body/)
*   **Response Status Code:** [https://fastapi.tiangolo.com/tutorial/response-status-code/](https://fastapi.tiangolo.com/tutorial/response-status-code/)
*   **Error Handling:** [https://fastapi.tiangolo.com/tutorial/handling-errors/](https://fastapi.tiangolo.com/tutorial/handling-errors/)
*   **CORS (Cross-Origin Resource Sharing):** [https://fastapi.tiangolo.com/tutorial/cors/](https://fastapi.tiangolo.com/tutorial/cors/)
*   **Testing:** [https://fastapi.tiangolo.com/tutorial/testing/](https://fastapi.tiangolo.com/tutorial/testing/)
