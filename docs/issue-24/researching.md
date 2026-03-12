# RESEARCHING - Issue #24

## Research Findings
Based on the issue description, the task is to create a main server entry point using FastAPI to serve both a REST API and a static frontend.

**1. Serving Static Files and `index.html` with FastAPI:**
The official FastAPI documentation provides a clear pattern for this use case.
-   **Mounting `StaticFiles`:** To serve a directory of static assets (like CSS, JS, and images), the `app.mount()` method is used. The syntax `app.mount("/static", StaticFiles(directory="path/to/static"), name="static")` is the standard approach. This makes all files in the specified directory available under the `/static` URL path.
-   **Serving a Single HTML File:** For a single-page application (SPA), it's common to serve an `index.html` file on the root path (`/`). The recommended way to do this in FastAPI is by creating a specific route (`@app.get("/")`) that returns a `fastapi.responses.FileResponse`.

This combined approach allows FastAPI to handle API requests (defined via decorators like `@app.get`, `@app.post`) and also serve the frontend files from the same server process, which is ideal for simple applications.

**2. Running the Application with Uvicorn:**
`uvicorn` is the recommended ASGI server for running FastAPI applications. The issue requests using `uvicorn.run(app, host="0.0.0.0", port=8000)` inside an `if __name__ == "__main__"` block. This is a common pattern for making a Python script directly executable for development purposes. The `host="0.0.0.0"` argument makes the server accessible on the local network, not just on localhost.

**3. Testing a FastAPI Application:**
FastAPI documentation recommends using `fastapi.testclient.TestClient`. This class provides an interface that mimics the `requests` library, allowing you to make HTTP requests directly to your app in a testing environment without needing a running server.
-   You instantiate the client with your FastAPI app instance: `client = TestClient(app)`.
-   You can then make requests: `response = client.get("/")`.
-   The `response` object allows you to inspect the status code (`response.status_code`), headers, and body (`response.text` or `response.json()`).

## Duplication Check
The repository does not contain any existing web server code using FastAPI or a similar framework. The `EXPLORING Output` correctly notes that `dashboard/app.py` uses Streamlit, which is a different web framework used for a separate data dashboard and does not follow the API/static file serving pattern required here. The rest of the codebase consists of the core logic for an AI agent and its supporting tools.

Therefore, this functionality is entirely new, and no existing code can be reused or refactored. The new `webapp` package will be a distinct new component.

## Recommended Approach
The approach outlined in the issue description is the correct and standard way to implement this functionality with FastAPI.

1.  **Create `webapp/server.py`:**
    *   This file should import the `app` instance from `webapp.api`. This decouples the server configuration from the API route definitions, which is good practice.
    *   Mount the static directory using `app.mount("/static", StaticFiles(directory="webapp/static"), name="static")`. The path `webapp/static` is correct, assuming the application is run from the project's root directory (e.g., `python -m webapp.server`).
    *   Define a route for `GET /` that returns `FileResponse("webapp/static/index.html")`. This will serve the frontend's main page.
    *   Include the `if __name__ == "__main__"` block to make the server runnable with `uvicorn.run(app, ...)`.

2.  **Create `tests/test_server.py`:**
    *   Import `TestClient` from `fastapi.testclient`.
    *   Import the `app` object from `webapp.server`.
    *   Instantiate the client: `client = TestClient(app)`.
    *   Create a test for the root path (`/`):
        *   Make a `client.get("/")` call.
        *   Assert that `response.status_code` is `200`.
        *   Assert that the response body contains the expected title, e.g., `b"ToDo List" in response.content`.
    *   Create an integration test for an API endpoint (`/api/todos`):
        *   Make a `client.get("/api/todos")` call.
        *   Assert that `response.status_code` is `200`.
        *   Assert that `response.json()` returns a list, confirming the response is valid JSON and has the expected top-level type.

This approach is modular, testable, and directly follows the best practices recommended in the FastAPI documentation.

## Risks and Edge Cases
-   **Dependency on Uncreated Files:** The implementation of `webapp/server.py` and its tests depends on `webapp/api.py` and `webapp/static/index.html`, which do not yet exist. The code will fail if `webapp.api` cannot be imported or if `webapp/api.py` does not define an `app` object. Similarly, the `FileResponse` will fail if `index.html` is missing. The implementation must proceed assuming these files will be created in other tasks.
-   **File Path Relativity:** The paths `webapp/static` and `webapp/static/index.html` are relative to the project root. This is fine as long as the application and tests are run from the root directory, which is standard practice (e.g., `python -m webapp.server` or `pytest`). Using absolute paths constructed with `pathlib` could make it more robust but is likely unnecessary given the context.
-   **Test Failures Due to Content Mismatch:** The test assertion `b"ToDo List" in response.content` creates a tight coupling between the test and the content of `index.html`. If the title in the HTML file changes, the test will break.
-   **API Endpoint Behavior:** The test for `/api/todos` assumes the endpoint exists on the imported `app` and returns a JSON list. This is an integration test, and its failure could point to a problem in either `server.py` or the (currently non-existent) `api.py`.

## Sources
-   [FastAPI Documentation: Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)
-   [FastAPI Documentation: Testing](https://fastapi.tiangolo.com/tutorial/testing/)
-   [Uvicorn Documentation: Running programmatically](https://www.uvicorn.org/programmatic/)
