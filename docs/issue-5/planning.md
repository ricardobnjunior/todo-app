# PLANNING - Issue #5

## Architecture
The solution will create a main entry point for the web application using FastAPI. The architecture separates concerns by having a dedicated `webapp/server.py` file whose sole responsibility is to assemble the application components and run the server.

1.  **Application Core:** The core FastAPI `app` object, containing all API logic, is imported from `webapp.api`. This assumes `webapp.api` is created in a previous step and defines all the API endpoints (e.g., `/api/todos`).
2.  **Server Entry Point (`webapp/server.py`):** This new file will be the runnable script. It will:
    *   Import the `app` from `webapp.api`.
    *   Mount the `webapp/static` directory to serve static assets like CSS and JavaScript under the `/static` URL path.
    *   Create a specific route for `GET /` to serve the main `webapp/static/index.html` file using `FileResponse`. This is standard practice for Single-Page Applications (SPAs).
    *   Include a `if __name__ == "__main__"` block to start a `uvicorn` server, making the application launchable via `python -m webapp.server`.
3.  **Testing (`tests/test_server.py`):** A new test file will be created to verify the server configuration. It will use FastAPI's `TestClient` to make in-memory requests to the application, without needing a live server. This allows for fast and reliable testing of the integrated application (API + static files).

This design creates a clear and modular structure, where the API definition (`webapp.api`) is separate from the serving mechanism (`webapp.server.py`).

## Files to Create
### `webapp/server.py`
- **Description:** This file will be the main entry point for running the entire web application. It combines the API from `webapp.api` with the static frontend files.
- **Contents:**
  - Import `uvicorn`, `StaticFiles` from `fastapi.staticfiles`, and `FileResponse` from `fastapi.responses`.
  - Import the `app` instance from `webapp.api`.
  - Mount the static directory at the `/static` path: `app.mount("/static", StaticFiles(directory="webapp/static"), name="static")`.
  - Define an asynchronous function for the `GET /` route that returns a `FileResponse` pointing to `webapp/static/index.html`.
  - Include an `if __name__ == "__main__"` block to start the server using `uvicorn.run(app, host="0.0.0.0", port=8000)`.

### `tests/test_server.py`
- **Description:** This file will contain integration tests for the `webapp.server` to ensure the API and frontend are served correctly.
- **Contents:**
  - Import `TestClient` from `fastapi.testclient`.
  - Import the `app` object from `webapp.server`.
  - Instantiate the client: `client = TestClient(app)`.
  - **`test_serve_index_html()` function:**
    - Makes a `GET` request to `/`.
    - Asserts that the response status code is `200`.
    - Asserts that the response text (HTML body) contains the string "ToDo List".
  - **`test_serve_api()` function:**
    - Makes a `GET` request to `/api/todos`.
    - Asserts that the response status code is `200`.
    - Asserts that the response JSON payload is an instance of `list`.

## Files to Modify
There are no files to modify for this issue.

## TODO List
1.  **Create file `webapp/server.py`** - simple
2.  **In `webapp/server.py`, add necessary imports** (`uvicorn`, `StaticFiles`, `FileResponse`, and `app` from `webapp.api`) - simple
3.  **In `webapp/server.py`, mount the static files directory** using `app.mount()` - simple
4.  **In `webapp/server.py`, define the root `GET /` route** to serve `index.html` via `FileResponse` - simple
5.  **In `webapp/server.py`, add the `if __name__ == "__main__"` block** to run `uvicorn` - simple
6.  **Create file `tests/test_server.py`** - simple
7.  **In `tests/test_server.py`, add imports and initialize `TestClient`** - simple
8.  **In `tests/test_server.py`, implement `test_serve_index_html()`** to test the root endpoint - simple
9.  **In `tests/test_server.py`, implement `test_serve_api()`** to test the `api/todos` endpoint - simple

## Test Plan
- **Unit/Integration Tests:**
  - The new file `tests/test_server.py` will contain tests using `TestClient`.
  - **Test Root Endpoint:** A test will send a `GET` request to `/`. It will verify that the HTTP status code is 200 and that the returned HTML content includes the text "ToDo List". This confirms that `index.html` is being served correctly.
  - **Test API Endpoint:** A test will send a `GET` request to `/api/todos`. It will verify that the HTTP status code is 200 and that the response body is a JSON array (`list` in Python). This confirms that the API application from `webapp.api` has been successfully integrated.

- **Manual E2E Test (to be performed after all related issues are completed):**
  1.  Run the application using the command `python -m webapp.server`.
  2.  Open a web browser and navigate to `http://localhost:8000`.
  3.  **Verify:** The ToDo list application page loads correctly.
  4.  **Verify:** You can add a new task, and it appears in the list.
  5.  **Verify:** You can delete a task, and it is removed from the list.
