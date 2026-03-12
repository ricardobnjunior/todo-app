from __future__ import annotations

import pytest
from datetime import datetime
from webapp import storage


@pytest.fixture(autouse=True)
def reset_storage():
    """Reset the in-memory storage before each test."""
    storage.todos.clear()
    storage._next_id = 1


def test_add_todo():
    """
    Tests that add_todo creates a todo with the correct structure and adds it to storage.
    """
    title = "My first todo"
    new_todo = storage.add_todo(title)

    # Check returned structure
    assert isinstance(new_todo, dict)
    assert new_todo["id"] == 1
    assert new_todo["title"] == title
    assert "created_at" in new_todo

    # Check if created_at is a valid ISO 8601 string
    try:
        # Pydantic's default factory produces a string compatible with fromisoformat
        datetime.fromisoformat(new_todo["created_at"])
    except (ValueError, TypeError):
        pytest.fail(f"created_at '{new_todo['created_at']}' is not a valid ISO 8601 string")

    # Check if it was added to storage
    all_todos = storage.list_todos()
    assert len(all_todos) == 1
    assert all_todos[0] == new_todo


def test_list_todos():
    """
    Tests that list_todos returns all added items.
    """
    assert storage.list_todos() == []

    todo1 = storage.add_todo("First")
    todo2 = storage.add_todo("Second")

    all_todos = storage.list_todos()
    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos


def test_delete_existing_todo():
    """
    Tests that delete_todo removes an existing item and returns True.
    """
    todo_to_delete = storage.add_todo("To be deleted")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(todo_to_delete["id"])

    assert result is True
    assert len(storage.list_todos()) == 0


def test_delete_non_existent_todo():
    """
    Tests that delete_todo returns False when the item does not exist.
    """
    storage.add_todo("Should not be deleted")
    assert len(storage.list_todos()) == 1

    result = storage.delete_todo(999)  # Non-existent ID

    assert result is False
    assert len(storage.list_todos()) == 1


def test_id_auto_increment_after_deletion():
    """
    Tests that the ID counter increments correctly and does not reuse IDs after deletion.
    """
    todo1 = storage.add_todo("Item 1")
    todo2 = storage.add_todo("Item 2")
    todo3 = storage.add_todo("Item 3")

    # IDs should be 1, 2, 3
    assert todo1["id"] == 1
    assert todo2["id"] == 2
    assert todo3["id"] == 3

    # Delete the middle one
    deleted = storage.delete_todo(2)
    assert deleted is True

    # Add a new one
    todo4 = storage.add_todo("Item 4")

    # New ID should be 4, not 2
    assert todo4["id"] == 4

    # Check the final list of IDs
    current_todos = storage.list_todos()
    current_ids = [t["id"] for t in current_todos]
    assert current_ids == [1, 3, 4]
