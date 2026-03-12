"""
In-memory storage for the To-Do list application.

This module provides a simple, non-persistent storage mechanism for to-do items.
It is intended for demonstration purposes and will lose all data upon application restart.
"""

_todos: dict[int, dict] = {}
_next_id: int = 1


def get_all_todos() -> list[dict]:
    """Returns a list of all to-do items."""
    return list(_todos.values())


def add_todo(title: str) -> dict:
    """
    Adds a new to-do item to the storage.

    Args:
        title: The title of the to-do item.

    Returns:
        A dictionary representing the newly created to-do item.
    """
    global _next_id
    new_todo = {"id": _next_id, "title": title}
    _todos[_next_id] = new_todo
    _next_id += 1
    return new_todo


def delete_todo(todo_id: int) -> dict | None:
    """
    Deletes a to-do item by its ID.

    Args:
        todo_id: The ID of the to-do item to delete.

    Returns:
        The deleted to-do item if found, otherwise None.
    """
    if todo_id in _todos:
        return _todos.pop(todo_id)
    return None


def _reset_storage():
    """
    Resets the in-memory storage to its initial state.
    This function is intended for testing purposes.
    """
    global _todos, _next_id
    _todos.clear()
    _next_id = 1
