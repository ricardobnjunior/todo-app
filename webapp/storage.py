"""
In-memory storage for ToDo items.

This module provides a simple, non-persistent storage layer for ToDo tasks.
The data is stored in a module-level list.
"""
from datetime import datetime, timezone
from typing import List, Dict, Any

# In-memory database for todos
todos: List[Dict[str, Any]] = []

# Counter for generating unique todo IDs
_next_id: int = 1


def add_todo(title: str) -> Dict[str, Any]:
    """
    Creates a new todo, adds it to the in-memory list, and returns it.

    Args:
        title: The title of the todo task.

    Returns:
        A dictionary representing the newly created todo.
    """
    global _next_id
    new_todo = {
        "id": _next_id,
        "title": title,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    todos.append(new_todo)
    _next_id += 1
    return new_todo


def list_todos() -> List[Dict[str, Any]]:
    """
    Returns the complete list of todos.

    Returns:
        A copy of the list of all todo items.
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
    initial_length = len(todos)
    todos = [todo for todo in todos if todo.get("id") != todo_id]
    return len(todos) < initial_length
