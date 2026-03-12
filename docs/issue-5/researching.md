# RESEARCHING - Issue #5

## Research Findings
The task is to create a single FastAPI server that serves both a REST API and a static frontend. This is a very common pattern for web applications. The official FastAPI documentation provides clear guidance on how to achieve this.

1.  **Serving Static Files:** The recommended way to serve a directory of static files (like CSS, JS, images) is by using `fastapi.staticfiles.StaticFiles`. The issue's requirement, `app.mount("/static", StaticFiles(directory="webapp/static"), name="static")`, is the standard and correct approach. Mounting at `/static` means any file in the `webapp/static` directory, like `styles.css`, will be available at the URL `/static/styles.css`.

2.  **Serving the Main HTML File:** To serve the main `index.html` file at the root path (`/`), using `fastapi.responses.FileResponse` is an excellent and efficient choice. It streams the file directly from the disk to the client. This is suitable for single-page applications (SPAs) where a single HTML file is the main entry point.

3.  **Application Structure:** The common practice is to have a central FastAPI application object. Other parts of the application, like API routers, can be included or mounted onto this central app. The issue specifies importing an `app` from `webapp.api` and then adding the static file routes to it. This is a clean, modular approach: `webapp.api` defines the API logic, and `webapp.server` handles the serving logic, combining the API with the frontend.

4.  **Running the Server:** The `if __name__ == "__main__"` block with a call to `uvicorn.run(app, ...)` is the standard method for creating an executable entry point for a web application for development purposes. The arguments `host="0.0.0.0"` and `port=8000` are correct for making the server accessible on the local network at the standard development port.

5.  **Testing:** FastAPI applications are tested using `fastapi.testclient.TestClient`. This client allows making requests to the application in-memory without needing to run a live server.
    *   Testing a `FileResponse` involves checking the status code (200) and inspecting the response content (e.g., `response.text` or `response.content`) to ensure the correct HTML is returned.
    *   Testing an API endpoint involves checking the status code and using `response.json()` to parse and validate the JSON payload.

## Duplication Check
The codebase does not contain any existing FastAPI or other web server implementations. The file `dashboard/app.py` uses Streamlit, which is a different framework for creating data apps and does not overlap with the requirements here.

Several scripts in the `src` directory (e.g., `orchestrator.py`, `duplication_checker.py`) use the `if __name__ == "__main__":` pattern to provide a command-line entry point. The proposed `webapp/server.py` should follow this established pattern.

The test suite in `tests/` primarily contains unit tests that mock external services like GitHub or LLM clients. There are no existing web tests using a test client. Therefore, `tests/test_server.py` will introduce a new testing pattern to the project, but one that is standard for FastAPI applications.

## Recommended Approach
The recommended approach aligns directly with the issue's requirements, as they follow FastAPI best practices.

1.  **Create `webapp/server.py`:**
    *   Import the `app` object from `webapp.api`. This object will serve as the core of the application.
    *   Mount the static files directory by calling `app.mount("/static", StaticFiles(directory="webapp/static"), name="static")`. The path `webapp/static` assumes the server will be run from the project root.
    *   Define a root endpoint `app.get("/")` that returns a `FileResponse("webapp/static/index.html")`. This will serve the main page of the application.
    *   Include the `if __name__ == "__main__"` guard to run the server with `uvicorn.run(app, host="0.0.0.0", port=8000)`.

2.  **Create `tests/test_server.py`:**
    *   Import `TestClient` from `fastapi.testclient` and the `app` object from `webapp.server`.
    *   Instantiate the client: `client = TestClient(app)`.
    *   Create a test for the root endpoint (`/`). It should make a `GET` request, assert the status code is `200`, and assert that the response body contains a key string from the HTML, like `"<title>ToDo List</title>"`.
    *   Create a test for the API endpoint (`/api/todos`). It should make a `GET` request, assert the status code is `200`, and assert that the parsed JSON response (`response.json()`) is a list.

This approach is simple, modular, and directly follows the patterns recommended in the FastAPI documentation. It cleanly separates the API definition from the server configuration.

## Risks and Edge Cases
*   **Missing Dependencies:** The implementation relies on `webapp/api.py` and the `webapp/static/index.html` file. The `EXPLORING` output indicates these files are not in the current repository context. Their absence will cause `ImportError` or `FileNotFoundError` at runtime. The implementation should assume these files will be created by a preceding task.
*   **Path Resolution:** Using hardcoded paths like `"webapp/static"` assumes the application is always run from the project's root directory (e.g., via `python -m webapp.server`). If run from a different directory, it would fail. While more robust solutions exist (using `pathlib` or `os.path.dirname(__file__)`), the current requested approach is acceptable for this project's structure.
*   **API Behavior:** The test for `/api/todos` assumes this endpoint exists and is defined in the `app` imported from `webapp.api`. If the API route is different or requires authentication (unlikely at this stage), the test will fail. The test should be simple enough to just check for a successful response and the correct data type (a list).

## Sources
*   [FastAPI Documentation: Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)
*   [FastAPI Documentation: Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
*   [FastAPI Documentation: Testing](https://fastapi.tiangolo.com/tutorial/testing/)
*   [Uvicorn Documentation: Programmatic running](https://www.uvicorn.org/programmatic/)
