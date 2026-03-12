"""
Tests for the in-memory To-Do storage.
"""

import importlib
import pytest
from datetime import datetime, timezone

# Import the module to be tested
from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage():
    """
    Fixture to reset the storage module's state before each test.
    This ensures that tests are isolated from each other.
    """
    importlib.reload(storage)


def test_add_todo():
    """
    Verifies that adding a todo returns the correct structure and persists the item.
    """
    title = "Buy milk"
    
    # 1. Add a new todo
    new_todo = storage.add_todo(title)
    
    # 2. Verify the returned dictionary structure and content
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo
    assert isinstance(new_todo["created_at"], str)
    
    # Verify the timestamp is a valid ISO 8601 format
    try:
        datetime.fromisoformat(new_todo["created_at"].replace('Z', '+00:00'))
    except ValueError:
        pytest.fail("created_at is not a valid ISO 8601 timestamp")

    # 3. Verify the item is in the main list
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos():
    """
    Verifies that listing todos returns all added items.
    """
    # Initially, the list should be empty
    assert storage.list_todos() == []

    # Add two items
    todo1 = storage.add_todo("First task")
    todo2 = storage.add_todo("Second task")

    # List todos and verify
    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert all_todos == [todo1, todo2]


def test_delete_todo_existing():
    """
    Verifies that deleting an existing todo returns True and removes it from the list.
    """
    # 1. Add a todo
    todo = storage.add_todo("Task to be deleted")
    assert len(storage.list_todos()) == 1

    # 2. Delete the todo
    result = storage.delete_todo(todo["id"])

    # 3. Verify the result and the state of the list
    assert result is True
    assert len(storage.list_todos()) == 0


def test_delete_todo_non_existent():
    """
    Verifies that deleting a non-existent todo returns False and doesn't change the list.
    """
    # 1. Add a todo
    storage.add_todo("An existing task")
    assert len(storage.list_todos()) == 1

    # 2. Attempt to delete a non-existent todo
    result = storage.delete_todo(999) # An ID that does not exist

    # 3. Verify the result and the state of the list
    assert result is False
    assert len(storage.list_todos()) == 1


def test_id_auto_increment():
    """
    Verifies that IDs auto-increment correctly, even after deletions.
    IDs should be 1, 2, 3 -> delete 2 -> add new -> new ID is 4.
    """
    # 1. Add three todos and check their IDs
    todo1 = storage.add_todo("Task 1")
    todo2 = storage.add_todo("Task 2")
    todo3 = storage.add_todo("Task 3")
    assert todo1["id"] == 1
    assert todo2["id"] == 2
    assert todo3["id"] == 3

    # 2. Delete the middle one
    delete_result = storage.delete_todo(2)
    assert delete_result is True

    # 3. Check the current list of IDs
    current_ids = [t["id"] for t in storage.list_todos()]
    assert current_ids == [1, 3]

    # 4. Add another todo
    todo4 = storage.add_todo("Task 4")

    # 5. Verify the new ID is 4 (and not 2)
    assert todo4["id"] == 4

    # 6. Verify the final list of IDs
    final_ids = [t["id"] for t in storage.list_todos()]
    assert final_ids == [1, 3, 4]
