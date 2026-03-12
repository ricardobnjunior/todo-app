from __future__ import annotations

from .models import Todo

# In-memory storage for todos
todos: list[dict] = []

# Counter for generating unique todo IDs
_next_id: int = 1


def add_todo(title: str) -> dict:
    """
    Creates a new todo with an auto-incremented ID and a timestamp,
    adds it to the in-memory list, and returns it.

    Args:
        title: The title of the todo task.

    Returns:
        A dictionary representing the newly created todo.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    _next_id += 1

    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    return todo_dict


def list_todos() -> list[dict]:
    """
    Returns a copy of the list of all todos.

    Returns:
        A list of dictionaries, where each dictionary represents a todo.
    """
    return todos.copy()


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a todo by its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was found and deleted, False otherwise.
    """
    global todos
    original_len = len(todos)
    # Rebuild the list in place, excluding the todo with the matching id
    todos[:] = [t for t in todos if t['id'] != todo_id]
    return len(todos) < original_len
