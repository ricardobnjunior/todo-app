import re
from datetime import datetime, timezone

import pytest

from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage():
    """
    This fixture automatically runs before each test to ensure a clean state.
    It clears the list of todos and resets the ID counter.
    """
    storage.todos.clear()
    storage._next_id = 1


def test_add_todo():
    """
    Tests that adding a todo returns a correctly structured dictionary
    and successfully adds it to the storage list.
    """
    title = "Buy groceries"
    new_todo = storage.add_todo(title)

    # 1. Verify the structure and content of the returned dictionary
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo

    # 2. Verify the timestamp is a valid ISO 8601 string and is recent
    try:
        created_time = datetime.fromisoformat(new_todo["created_at"])
        assert created_time.tzinfo is not None
        time_difference = datetime.now(timezone.utc) - created_time
        assert time_difference.total_seconds() < 2
    except (ValueError, TypeError):
        pytest.fail("created_at is not a valid ISO 8601 timestamp string.")

    # 3. Verify the internal state of the storage module
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo
    assert storage._next_id == 2


def test_list_todos():
    """
    Tests that listing todos returns all items that have been added.
    """
    # Initially, the list should be empty
    assert storage.list_todos() == []

    # Add items and verify they are listed correctly
    todo1 = storage.add_todo("First task")
    todo2 = storage.add_todo("Second task")

    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos


def test_delete_existing_todo():
    """
    Tests that deleting an existing todo returns True and removes the
    item from the list.
    """
    todo1 = storage.add_todo("Task to be deleted")
    todo2 = storage.add_todo("Task to keep")

    result = storage.delete_todo(todo1["id"])

    # Verify the function returned True
    assert result is True

    # Verify the item was removed from storage
    remaining_todos = storage.list_todos()
    assert len(remaining_todos) == 1
    assert remaining_todos[0] == todo2


def test_delete_non_existent_todo():
    """
    Tests that attempting to delete a non-existent todo returns False
    and does not alter the storage list.
    """
    storage.add_todo("A single task")

    result = storage.delete_todo(999)  # A non-existent ID

    # Verify the function returned False
    assert result is False

    # Verify the storage list is unchanged
    all_todos = storage.list_todos()
    assert len(all_todos) == 1


def test_ids_auto_increment_correctly():
    """
    Tests that IDs are unique and increment correctly, even after
    items have been deleted from the middle of the list.
    """
    # Add three items, IDs should be 1, 2, 3
    t1 = storage.add_todo("Task 1")
    t2 = storage.add_todo("Task 2")
    t3 = storage.add_todo("Task 3")

    assert t1["id"] == 1
    assert t2["id"] == 2
    assert t3["id"] == 3
    assert storage._next_id == 4

    # Delete the middle item
    was_deleted = storage.delete_todo(2)
    assert was_deleted is True

    # Add a new item
    t4 = storage.add_todo("Task 4")

    # The new ID should continue from the counter (4), not fill the gap (2)
    assert t4["id"] == 4
    assert storage._next_id == 5

    # Check the final state of IDs in the list
    final_todos = storage.list_todos()
    final_ids = [t["id"] for t in final_todos]
    assert sorted(final_ids) == [1, 3, 4]
