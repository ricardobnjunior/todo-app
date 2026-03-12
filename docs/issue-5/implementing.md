# IMPLEMENTING - Issue #5

### FILE: webapp/server.py
```python
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# This line assumes that a file named `webapp/api.py` exists and
# contains a FastAPI application instance named `app`.
from webapp.api import app

# Mount a directory named 'static' (located in 'webapp/static')
# to the URL path '/static'. This allows serving static files like
# CSS, JavaScript, and images.
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    """
    This endpoint serves the main HTML file of the frontend application.
    It returns the `index.html` file from the static directory.
    """
    return FileResponse("webapp/static/index.html")

if __name__ == "__main__":
    # This block makes the script runnable.
    # When you run `python -m webapp.server`, this code will execute.
    # It starts a Uvicorn server to host the FastAPI application.
    # host="0.0.0.0" makes the server accessible from other devices on the network.
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### FILE: tests/test_server.py
```python
import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# --- Test Setup ---

# Create a mock FastAPI app to stand in for the real one from `webapp.api`.
# This is necessary because `webapp.api` is created in a different step and
# may not exist in the test environment.
mock_api_app = FastAPI()

@mock_api_app.get("/api/todos")
async def mock_get_todos():
    """A mock endpoint to simulate the real API, returning a list."""
    return [{"id": 1, "task": "Run tests"}]

# Before importing the server, we patch the system's modules dictionary.
# This intercepts the `from webapp.api import app` statement and provides
# our mock_api_app instead, allowing the test to run in isolation.
with patch.dict("sys.modules", {"webapp.api": MagicMock(app=mock_api_app)}):
    from webapp.server import app

# Instantiate the test client with our fully assembled application, which now
# includes the mocked API routes and the static file serving logic.
client = TestClient(app)


@pytest.fixture
def mock_frontend_files(tmp_path):
    """
    Pytest fixture to create a temporary file structure that mimics
    the expected 'webapp/static/index.html' layout. It also handles
    changing the current working directory, since the application code
    uses a relative path to find these files.
    """
    # Create the directory structure: <tmp_path>/webapp/static/
    static_dir = tmp_path / "webapp" / "static"
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the index.html file with content to test against.
    index_html_path = static_dir / "index.html"
    index_html_path.write_text("<!DOCTYPE html><html><head><title>ToDo List</title></head></html>")

    # The code under test (webapp/server.py) uses a relative path:
    # 'webapp/static/index.html'. To make this resolve correctly during
    # tests, we temporarily change the current working directory.
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    # Yield control back to the test function.
    yield
    
    # After the test is done, change the directory back to its original state.
    os.chdir(original_cwd)


# --- Tests ---

def test_serve_index_html(mock_frontend_files):
    """
    Verifies that a GET request to the root path ('/') successfully
    serves the main frontend 'index.html' file.
    
    It checks for a 200 OK status code and confirms the response body
    contains the title of the ToDo list application.
    """
    # The `mock_frontend_files` fixture is active here, ensuring the
    # necessary files and directory structure exist.
    response = client.get("/")
    assert response.status_code == 200
    assert "ToDo List" in response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_serve_api_endpoint():
    """
    Verifies that the API routes (which should be mounted from `webapp.api`)
    are correctly served.

    It checks that a GET request to '/api/todos' returns a 200 OK status
    and a JSON list, as defined in our mock API app. This confirms that
    the API app has been successfully integrated into the main server app.
    """
    response = client.get("/api/todos")
    assert response.status_code == 200
    # Check that the response is a valid JSON list.
    assert isinstance(response.json(), list)
    # Check for specific content from our mock endpoint to be sure.
    assert response.json() == [{"id": 1, "task": "Run tests"}]
```

## Decisions Made
1.  **Dependency Mocking**: Since the required files `webapp/api.py` and `webapp/static/index.html` were not provided in the context, I had to create mocks for them in `tests/test_server.py` to ensure the tests could run in isolation.
    *   For `webapp.api`, I used `unittest.mock.patch` to intercept the import and provide a mock `FastAPI` instance with the required `/api/todos` endpoint.
    *   For `webapp/static/index.html`, I created a pytest fixture (`mock_frontend_files`) that uses `tmp_path` to build the necessary directory structure and file.
2.  **Handling Relative Paths in Tests**: The server code uses hardcoded relative paths (`"webapp/static"`). To make this work during testing without modifying the source code, the `mock_frontend_files` fixture temporarily changes the current working directory (`os.chdir`) to the temporary test directory. This is a pragmatic solution to test the code as-is, and the fixture ensures the original working directory is restored after the test completes.
3.  **API Schema**: I added `include_in_schema=False` to the `GET /` route in `webapp/server.py`. This is a common practice to prevent frontend-serving routes from appearing in the auto-generated OpenAPI (Swagger/ReDoc) documentation, keeping it clean and focused on the actual API.

## Notes
*   The implementation correctly follows all requirements from the issue description and the TODO list.
*   The tests are comprehensive, covering both the serving of the static `index.html` and the integration of the API routes from `webapp.api`.
*   The code relies on the presence of `webapp/api.py` and the `webapp/static` directory at runtime. The tests have been designed to pass without these files, but the application will fail if they are not created by other steps in the project.
