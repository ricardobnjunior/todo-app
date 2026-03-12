"""
Tests for the FastAPI ToDo list API.
"""

import pytest
from fastapi.testclient import TestClient

from webapp.api import app
from webapp import storage


@pytest.fixture(autouse=True)
def clean_storage_before_tests():
    """Fixture to ensure storage is reset before each test."""
    storage.reset_storage()


client = TestClient(app)


def test_create_and_get_todo():
    """
    Test creating a new todo via POST and then retrieving it via GET.
    """
    # 1. POST a new todo
    response_post = client.post(
        "/api/todos",
        json={"title": "First Todo"},
    )
    assert response_post.status_code == 201
    created_todo = response_post.json()
    assert "id" in created_todo
    assert created_todo["id"] == 1
    assert created_todo["title"] == "First Todo"

    # 2. GET all todos and verify the new one is there
    response_get = client.get("/api/todos")
    assert response_get.status_code == 200
    todos_list = response_get.json()
    assert len(todos_list) == 1
    assert todos_list[0]["id"] == created_todo["id"]
    assert todos_list[0]["title"] == created_todo["title"]


def test_delete_existing_todo():
    """
    Test deleting an existing todo.
    """
    # 1. Create a todo to delete
    response_post = client.post(
        "/api/todos",
        json={"title": "Todo to be deleted"},
    )
    assert response_post.status_code == 201
    todo_id = response_post.json()["id"]

    # 2. Delete the todo
    response_delete = client.delete(f"/api/todos/{todo_id}")
    assert response_delete.status_code == 200
    assert response_delete.json() == {"deleted": True}

    # 3. Verify it's gone
    response_get = client.get("/api/todos")
    assert response_get.status_code == 200
    assert response_get.json() == []


def test_delete_non_existent_todo():
    """
    Test that deleting a non-existent todo returns a 404 error.
    """
    # Attempt to delete a todo with an ID that doesn't exist
    response_delete = client.delete("/api/todos/999")
    assert response_delete.status_code == 404
    assert response_delete.json() == {"detail": "Todo not found"}
