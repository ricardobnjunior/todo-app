import pytest
from fastapi.testclient import TestClient

from webapp.api import app
from webapp import storage

# This fixture will be automatically used by all tests in this file
@pytest.fixture(autouse=True)
def reset_storage_before_each_test():
    """
    Resets the in-memory storage before each test function runs to ensure
    test isolation.
    """
    storage.reset_storage()

client = TestClient(app)

def test_create_and_get_todos():
    """
    Tests creating a new todo via POST and then retrieving the list via GET.
    """
    # 1. Initially, the list of todos should be empty
    initial_response = client.get("/api/todos")
    assert initial_response.status_code == 200
    assert initial_response.json() == []

    # 2. POST a new todo
    response = client.post("/api/todos", json={"title": "Test my new API"})
    assert response.status_code == 201, "Expected 201 Created for a new resource"
    
    created_todo = response.json()
    assert "id" in created_todo
    assert created_todo["id"] == 1
    assert created_todo["title"] == "Test my new API"

    # 3. GET all todos to verify the created todo is in the list
    get_response = client.get("/api/todos")
    assert get_response.status_code == 200
    
    todos_list = get_response.json()
    assert isinstance(todos_list, list)
    assert len(todos_list) == 1
    assert todos_list[0] == created_todo

def test_delete_todo():
    """
    Tests deleting an existing todo.
    """
    # 1. Create a todo to be deleted
    create_response = client.post("/api/todos", json={"title": "This will be deleted"})
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    # 2. Delete the todo
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"deleted": True}

    # 3. Verify the todo is gone by fetching the list again
    get_response = client.get("/api/todos")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0

def test_delete_nonexistent_todo():
    """
    Tests that attempting to delete a non-existent todo returns a 404 error.
    """
    response = client.delete("/api/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
