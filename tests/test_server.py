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
