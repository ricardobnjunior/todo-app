import pytest
from datetime import datetime
from webapp import storage

@pytest.fixture(autouse=True)
def reset_storage():
    """
    This fixture automatically runs before each test.
    It resets the in-memory storage to a clean state, ensuring
    that tests are isolated from each other.
    """
    storage.todos.clear()
    storage._next_id = 1
    # Yield control to the test function
    yield
    # Teardown (optional, but good practice if needed)
    storage.todos.clear()
    storage._next_id = 1

def test_add_todo():
    """
    Tests if add_todo creates a todo with the correct structure and data.
    """
    title = "My first test todo"
    new_todo = storage.add_todo(title)

    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo
    # Verify created_at is a valid ISO 8601 timestamp string
    try:
        datetime.fromisoformat(new_todo["created_at"])
    except (ValueError, TypeError):
        pytest.fail("created_at is not a valid ISO format string.")

    # Check if it was added to the list
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo

def test_list_todos():
    """
    Tests if list_todos returns all added items.
    """
    # Initially, the list should be empty
    assert storage.list_todos() == []

    # Add some todos
    todo1 = storage.add_todo("Task 1")
    todo2 = storage.add_todo("Task 2")

    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos

def test_delete_todo_success():
    """
    Tests if deleting an existing todo returns True and removes it from the list.
    """
    todo = storage.add_todo("To be deleted")
    todo_id = todo["id"]

    # The list should have one item before deletion
    assert len(storage.list_todos()) == 1

    # Delete the todo
    result = storage.delete_todo(todo_id)

    # Check if deletion was successful
    assert result is True
    assert len(storage.list_todos()) == 0

def test_delete_todo_not_found():
    """
    Tests that attempting to delete a non-existent todo returns False.
    """
    storage.add_todo("An existing todo")

    # Attempt to delete a todo with an ID that does not exist
    result = storage.delete_todo(999)

    assert result is False
    # Ensure the list was not modified
    assert len(storage.list_todos()) == 1

def test_id_auto_increments_correctly():
    """
    Tests that IDs auto-increment correctly, even after a deletion.
    IDs should be 1, 2, 3. Delete 2. Add new. IDs should be 1, 3, 4.
    """
    # Add three todos
    t1 = storage.add_todo("Task 1")
    t2 = storage.add_todo("Task 2")
    t3 = storage.add_todo("Task 3")

    assert t1["id"] == 1
    assert t2["id"] == 2
    assert t3["id"] == 3

    # Delete the middle todo
    storage.delete_todo(2)

    # Add another todo
    t4 = storage.add_todo("Task 4")

    # The new todo should have the next ID in sequence (4)
    assert t4["id"] == 4

    # Verify the final list of IDs
    current_ids = [todo["id"] for todo in storage.list_todos()]
    assert current_ids == [1, 3, 4]
