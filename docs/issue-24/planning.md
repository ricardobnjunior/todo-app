# PLANNING - Issue #24

## Architecture
The solution will establish a web application component within the project using FastAPI. The architecture separates the API definition from the server configuration.

1.  **`webapp/api.py`**: This new file will contain the core FastAPI application instance and define API-specific routes (e.g., `/api/todos`). For this issue, it will contain a minimal placeholder implementation to satisfy dependencies.
2.  **`webapp/static/`**: This new directory will house all static frontend assets. A placeholder `index.html` will be created here.
3.  **`webapp/server.py`**: This new file will be the main application entry point. It will import the FastAPI `app` from `webapp.api`, mount the `webapp/static` directory to serve frontend files, and define the root (`/`) route to serve `index.html`. It will also contain the `uvicorn` runner logic inside an `if __name__ == "__main__"` block, making the application executable.
4.  **`tests/test_server.py`**: This new test file will contain integration tests using `fastapi.testclient.TestClient` to verify that the assembled application correctly serves both the frontend entry point and the API endpoints.

This structure allows the API logic and the server/serving configuration to be managed independently, which is a robust pattern for web applications. The `webapp` directory will be configured as a Python package by adding an `__init__.py` file.

## Files to Create
-   **`webapp/__init__.py`**
    -   Description: An empty file to make the `webapp` directory a Python package, enabling module imports like `from webapp.api import app`.
-   **`webapp/api.py`**
    -   Description: Defines the core FastAPI application and its API routes. This is a dependency for `server.py`.
    -   Contents:
        -   A `FastAPI` instance named `app`.
        -   A route for `GET /api/todos` that returns an empty list, `[]`, to satisfy the test requirement.
-   **`webapp/static/index.html`**
    -   Description: The main HTML file for the single-page frontend application. It is served by the root route and is a dependency for both the server and the tests.
    -   Contents: A minimal HTML5 document with `<title>ToDo List</title>` and "ToDo List" in the body to pass the tests.
-   **`webapp/server.py`**
    -   Description: The main server entry point that assembles the API and static file serving.
    -   Contents:
        -   Import `app` from `webapp.api`.
        -   Mount the `webapp/static` directory at the `/static` path.
        -   Define a `GET /` route that returns `webapp/static/index.html` using `FileResponse`.
        -   An `if __name__ == "__main__"` block to run the app with `uvicorn`.
-   **`tests/test_server.py`**
    -   Description: Contains integration tests for the web application server.
    -   Contents:
        -   A `TestClient` instance initialized with the `app` from `webapp.server`.
        -   A test case for `GET /` to check for a 200 status and "ToDo List" in the response body.
        -   A test case for `GET /api/todos` to check for a 200 status and a JSON list response.

## Files to Modify
There are no existing files to modify for this issue. The work is entirely additive, creating a new `webapp` component.

## TODO List
1.  Create the `webapp` directory. - simple
2.  Create the `webapp/static` directory. - simple
3.  Create `webapp/__init__.py` as an empty file. - simple
4.  Create `webapp/static/index.html` with minimal HTML and the text "ToDo List". - simple
5.  Create `webapp/api.py` with a FastAPI app instance and a placeholder `GET /api/todos` endpoint. - simple
6.  Create `webapp/server.py`, import the app from `api.py`, mount the static directory, add the root route, and include the `uvicorn` runner. - medium
7.  Create `tests/test_server.py` and set up the `TestClient`. - simple
8.  In `tests/test_server.py`, implement the test for the `GET /` endpoint, asserting status code and HTML content. - medium
9.  In `tests/test_server.py`, implement the test for the `GET /api/todos` endpoint, asserting status code and JSON response. - medium

## Test Plan
-   **Automated Integration Tests (`tests/test_server.py`)**:
    -   **Test Root Endpoint**:
        -   **Action**: Send a `GET` request to `/`.
        -   **Expected**: The server should respond with a `200 OK` status. The response body should be HTML content containing the text "ToDo List".
    -   **Test API Endpoint**:
        -   **Action**: Send a `GET` request to `/api/todos`.
        -   **Expected**: The server should respond with a `200 OK` status. The response body should be a valid JSON array (e.g., `[]`).
-   **Manual Execution Test**:
    -   **Action**: Once all related issues for the webapp are complete, run `python -m webapp.server` from the project root.
    -   **Expected**: The application should start and be accessible at `http://localhost:8000`. Opening this URL in a web browser should display the full ToDo list application, and it should be functional (allowing tasks to be added and deleted). This validates that the server, API, and static files work together correctly in a live environment.
