"""
Tests for the FastAPI To-Do list API.

These tests use the FastAPI TestClient to make requests to the application
and verify the behavior of the API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from webapp import storage
from webapp.api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage_before_each_test():
    """
    Fixture to reset the in-memory storage before each test.
    `autouse=True` ensures it runs automatically for every test function,
    guaranteeing test isolation.
    """
    storage._reset_storage()
    yield  # The test runs here


def test_create_todo():
    """
    Tests POST /api/todos to ensure a new todo can be created.
    """
    response = client.post("/api/todos", json={"title": "Test Todo"})
    assert response.status_code == 201, "Should return 201 CREATED"
    data = response.json()
    assert data["title"] == "Test Todo"
    assert "id" in data
    assert data["id"] == 1


def test_get_todos():
    """
    Tests GET /api/todos to ensure it returns a list of all todos.
    """
    # First, create some todos to populate the storage
    client.post("/api/todos", json={"title": "First Todo"})
    client.post("/api/todos", json={"title": "Second Todo"})

    # Then, get the list of todos
    response = client.get("/api/todos")
    assert response.status_code == 200, "Should return 200 OK"
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "First Todo"
    assert data[0]["id"] == 1
    assert data[1]["title"] == "Second Todo"
    assert data[1]["id"] == 2


def test_delete_existing_todo():
    """
    Tests DELETE /api/todos/{todo_id} for an existing todo.
    """
    # Create a todo to delete
    create_response = client.post("/api/todos", json={"title": "To be deleted"})
    todo_id = create_response.json()["id"]

    # Delete the todo
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200, "Should return 200 OK"
    assert delete_response.json() == {"deleted": True}

    # Verify it's gone by fetching all todos
    get_response = client.get("/api/todos")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0, "The todo list should be empty"


def test_delete_non_existent_todo():
    """
    Tests DELETE /api/todos/{todo_id} for a non-existent todo.
    """
    response = client.delete("/api/todos/999")
    assert response.status_code == 404, "Should return 404 NOT FOUND"
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo_with_empty_title_fails():
    """
    Tests that creating a todo with an empty title is rejected.
    Pydantic should return a 422 Unprocessable Entity error.
    """
    # A title with just whitespace should also be considered.
    # The default Pydantic model with `min_length=1` handles this.
    response = client.post("/api/todos", json={"title": ""})
    assert response.status_code == 422, "Should return 422 UNPROCESSABLE ENTITY"
