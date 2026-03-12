# IMPLEMENTING - Issue #24

### FILE: webapp/__init__.py
```python
# This file makes the 'webapp' directory a Python package.

```

### FILE: webapp/api.py
```python
"""
This module contains the API routes for the ToDo application.
The main FastAPI application instance is created here.
"""
from fastapi import FastAPI

# The main FastAPI app instance for the API.
# The server.py file will import this and add frontend serving capabilities.
app = FastAPI()

# Placeholder in-memory "database".
# In a real application, this would be replaced by a proper database connection.
# For the purpose of these issues, it will be expanded to a more stateful manager.
todos_db = []


@app.get("/api/todos")
async def get_todos():
    """
    Returns the list of all ToDo items.
    """
    return todos_db

```

### FILE: webapp/server.py
```python
"""
This is the main server entry point for the ToDo list application.

It combines the API defined in `webapp.api` with static file serving for the frontend.
Running this script will start the Uvicorn server for development.
"""
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import the FastAPI app instance from the api module.
# This instance contains all the API routes.
from webapp.api import app


# Mount the 'static' directory, which contains the frontend files (HTML, CSS, JS).
# These files will be served under the '/static' path.
# The path "webapp/static" is relative to the project root where the server is run.
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")


@app.get("/")
async def read_index():
    """
    Serves the main index.html file.
    This is the entry point for the single-page frontend application.
    """
    return FileResponse("webapp/static/index.html")


if __name__ == "__main__":
    # This block allows running the server directly using `python -m webapp.server`.
    # It's intended for development purposes. For production, a proper ASGI server
    # like Gunicorn with Uvicorn workers should be used.
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

### FILE: webapp/static/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ToDo List</title>
</head>
<body>
    <h1>ToDo List</h1>
    <p>Application entry point. The actual content will be rendered by JavaScript.</p>
</body>
</html>
```

### FILE: tests/test_server.py
```python
"""
Tests for the main server which combines API and static file serving.
"""
from fastapi.testclient import TestClient

# Import the 'app' from the server module, which is the final, assembled
# FastAPI application including both API routes and static file mounts.
from webapp.server import app

# Create a TestClient instance to make requests to the app in tests.
client = TestClient(app)


def test_read_root():
    """
    Test that the root path ('/') serves the index.html file successfully.
    """
    response = client.get("/")
    assert response.status_code == 200
    # Check for content that is expected to be in our placeholder index.html
    assert "ToDo List" in response.text
    assert "<h1>ToDo List</h1>" in response.text


def test_get_todos_api_endpoint():
    """
    Test the GET /api/todos endpoint to ensure it's wired up correctly.
    This is an integration test that checks if the API imported from `webapp.api`
    is reachable through the `webapp.server` app.
    """
    response = client.get("/api/todos")
    assert response.status_code == 200
    # The placeholder API should return an empty list initially.
    assert response.json() == []

```

## Decisions Made
1.  **Placeholder `webapp/api.py`**: The plan mentioned creating a placeholder `api.py`. I implemented this with a FastAPI app instance and a single `GET /api/todos` endpoint that returns an empty list. This is sufficient to satisfy the dependencies for `server.py` and the tests, allowing this issue to be self-contained.
2.  **Placeholder `webapp/static/index.html`**: Similarly, I created a minimal `index.html` file containing the text "ToDo List". This allows the root endpoint (`/`) and its corresponding test to pass.
3.  **Path Relativity**: The file paths in `server.py` (`directory="webapp/static"` and `FileResponse("webapp/static/index.html")`) are relative to the project root. This is standard and works correctly when running the server with `python -m webapp.server` or running tests with `pytest` from the root directory.
4.  **Importing `app` in `tests/test_server.py`**: The tests import the `app` object from `webapp.server`, not `webapp.api`. This is the correct approach as `webapp.server.app` is the final, composed application that includes the static file serving logic which needs to be tested.

## Notes
The implementation creates a new `webapp` package and its server entry point as requested. The created files include placeholders (`webapp/api.py`, `webapp/static/index.html`) which are expected to be replaced or built upon in subsequent issues. The tests confirm that the server correctly serves both the frontend's entry point and the API endpoint as required.
