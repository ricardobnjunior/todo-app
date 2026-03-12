"""
In-memory storage for ToDo items.
This is a simple implementation for demonstration purposes and is not thread-safe.
"""

_TODOS = {}
_NEXT_ID = 1


def reset_storage():
    """Resets the in-memory storage to its initial empty state."""
    global _TODOS, _NEXT_ID
    _TODOS = {}
    _NEXT_ID = 1


def get_all_todos() -> list[dict]:
    """Returns a list of all ToDo items."""
    return list(_TODOS.values())


def add_todo(title: str) -> dict:
    """
    Adds a new ToDo item to the storage.

    Args:
        title: The title of the ToDo item.

    Returns:
        The newly created ToDo item as a dictionary.
    """
    global _NEXT_ID
    todo_id = _NEXT_ID
    _TODOS[todo_id] = {"id": todo_id, "title": title}
    _NEXT_ID += 1
    return _TODOS[todo_id]


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a ToDo item by its ID.

    Args:
        todo_id: The ID of the ToDo item to delete.

    Returns:
        True if the item was found and deleted, False otherwise.
    """
    if todo_id in _TODOS:
        del _TODOS[todo_id]
        return True
    return False
