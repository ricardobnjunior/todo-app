"""
Tests for the in-memory storage module.
"""
import pytest
from datetime import datetime, timezone, timedelta

from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage_state():
    """
    A fixture that automatically runs before each test to reset the storage.
    This ensures that tests are isolated and don't interfere with each other.
    """
    storage.todos.clear()
    # Resetting a non-public variable is generally discouraged, but necessary
    # for testing this specific implementation.
    storage._next_id = 1
    yield


def test_add_todo():
    """
    Tests that add_todo correctly creates a task, returns it, and stores it.
    """
    title = "My first task"
    new_todo = storage.add_todo(title=title)

    # 1. Check the returned dictionary
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo

    # Check if a valid ISO timestamp was created
    created_at_dt = datetime.fromisoformat(new_todo["created_at"])
    assert created_at_dt.tzinfo is not None
    # Check if the timestamp is recent (within the last 5 seconds)
    assert datetime.now(timezone.utc) - created_at_dt < timedelta(seconds=5)

    # 2. Check the side effect (storage)
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos():
    """
    Tests that list_todos returns all added items.
    """
    assert storage.list_todos() == []  # Should be empty initially

    storage.add_todo("Task 1")
    storage.add_todo("Task 2")
    storage.add_todo("Task 3")

    all_todos = storage.list_todos()
    assert len(all_todos) == 3
    assert all_todos[0]["id"] == 1
    assert all_todos[1]["title"] == "Task 2"
    assert all_todos[2]["id"] == 3


def test_delete_existing_todo():
    """
    Tests that delete_todo with an existing ID returns True and removes the item.
    """
    todo = storage.add_todo("Task to be deleted")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(todo["id"])
    assert result is True
    assert len(storage.list_todos()) == 0


def test_delete_non_existent_todo():
    """
    Tests that delete_todo with a non-existent ID returns False.
    """
    storage.add_todo("An existing task")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(999)  # A non-existent ID
    assert result is False
    assert len(storage.list_todos()) == 1


def test_id_auto_increment_after_deletion():
    """
    Tests that IDs auto-increment correctly even after an item is deleted.
    IDs should be 1, 3, 4 after adding 3, deleting the middle one, and adding one more.
    """
    # Add three todos
    t1 = storage.add_todo("Task 1")
    t2 = storage.add_todo("Task 2")
    t3 = storage.add_todo("Task 3")
    assert [t["id"] for t in storage.list_todos()] == [1, 2, 3]

    # Delete the middle one
    deleted = storage.delete_todo(t2["id"])
    assert deleted is True
    assert [t["id"] for t in storage.list_todos()] == [1, 3]

    # Add another one
    t4 = storage.add_todo("Task 4")
    assert t4["id"] == 4, "The next ID should be 4, not re-using 2"

    # Check final state of IDs
    final_ids = [t["id"] for t in storage.list_todos()]
    assert final_ids == [1, 3, 4]
