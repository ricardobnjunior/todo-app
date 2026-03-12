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
