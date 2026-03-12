from datetime import datetime
import pytest
from webapp import storage, models

@pytest.fixture(autouse=True)
def reset_storage_state():
    """
    This fixture automatically runs before each test function.
    It resets the in-memory storage to a clean state, ensuring
    that tests are isolated and don't interfere with each other.
    """
    storage.todos.clear()
    storage._next_id = 1


def test_add_todo_returns_correct_structure():
    """
    Tests that add_todo creates a todo with the correct structure and data.
    """
    title = "My First Task"
    new_todo = storage.add_todo(title)

    assert isinstance(new_todo, dict)
    assert 'id' in new_todo
    assert 'title' in new_todo
    assert 'created_at' in new_todo

    assert new_todo['id'] == 1
    assert new_todo['title'] == title

    # Verify that created_at is a valid ISO 8601 timestamp string
    try:
        datetime.fromisoformat(new_todo['created_at'])
    except (ValueError, TypeError):
        pytest.fail("created_at is not a valid ISO 8601 string.")

    # Verify the todo was actually added to the list
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos_returns_all_items():
    """
    Tests that list_todos returns all items that have been added.
    """
    storage.add_todo("Task 1")
    storage.add_todo("Task 2")
    storage.add_todo("Task 3")

    all_todos = storage.list_todos()
    assert len(all_todos) == 3
    assert all_todos[0]['title'] == "Task 1"
    assert all_todos[1]['id'] == 2
    assert all_todos[2]['title'] == "Task 3"


def test_delete_existing_todo():
    """
    Tests that delete_todo correctly removes an existing item and returns True.
    """
    todo1 = storage.add_todo("Task to be deleted")
    storage.add_todo("Task to keep")

    # Delete the first todo
    result = storage.delete_todo(todo1['id'])
    
    assert result is True

    # Verify it was removed
    remaining_todos = storage.list_todos()
    assert len(remaining_todos) == 1
    assert remaining_todos[0]['title'] == "Task to keep"


def test_delete_non_existent_todo():
    """
    Tests that delete_todo returns False when trying to delete an item that does not exist.
    """
    storage.add_todo("An existing task")

    # Try to delete a todo with an ID that doesn't exist
    result = storage.delete_todo(999)

    assert result is False

    # Verify the list remains unchanged
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0]['title'] == "An existing task"


def test_id_auto_increment_after_deletion():
    """
    Tests that the auto-incrementing ID continues from the last value,
    even after items have been deleted.
    """
    # Add three todos, they should get IDs 1, 2, 3
    storage.add_todo("Task 1")
    storage.add_todo("Task 2")
    storage.add_todo("Task 3")

    # Delete the middle todo (ID 2)
    deleted = storage.delete_todo(2)
    assert deleted is True

    # Add a new todo, it should get ID 4
    new_todo = storage.add_todo("Task 4")
    assert new_todo['id'] == 4
    
    # Verify the final state of the list
    final_todos = storage.list_todos()
    assert len(final_todos) == 3
    
    final_ids = [todo['id'] for todo in final_todos]
    assert final_ids == [1, 3, 4]

# Test for the model itself, just to be thorough.
def test_todo_model_defaults():
    """
    Tests that the Pydantic model correctly assigns default values.
    """
    todo = models.Todo(id=1, title="Test Title")
    
    assert todo.id == 1
    assert todo.title == "Test Title"
    assert isinstance(todo.created_at, str)
    
    # Check that the default factory produces a valid ISO timestamp
    try:
        datetime.fromisoformat(todo.created_at)
    except (ValueError, TypeError):
        pytest.fail("Default created_at is not a valid ISO 8601 string.")
