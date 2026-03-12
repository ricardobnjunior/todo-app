"""
In-memory storage for To-Do items.

This module provides a simple in-memory database for managing To-Do items.
The data is stored in a module-level list and will be reset when the
application restarts.
"""

from typing import List, Dict

from webapp.models import Todo

# In-memory database of To-Do items
todos: List[Dict] = []
_next_id: int = 1


def add_todo(title: str) -> Dict:
    """
    Creates a new To-Do item, adds it to the in-memory list, and returns it.

    Args:
        title: The title of the To-Do item.

    Returns:
        A dictionary representing the newly created To-Do item.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    
    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    
    _next_id += 1
    return todo_dict


def list_todos() -> List[Dict]:
    """
    Returns the list of all To-Do items.

    Returns:
        A list of dictionaries, where each dictionary is a To-Do item.
    """
    return todos[:]


def delete_todo(todo_id: int) -> bool:
    """
    Deletes a To-Do item by its ID.

    Args:
        todo_id: The ID of the To-Do item to delete.

    Returns:
        True if the item was found and deleted, False otherwise.
    """
    global todos
    todo_to_delete = None
    for todo in todos:
        if todo["id"] == todo_id:
            todo_to_delete = todo
            break
            
    if todo_to_delete:
        todos.remove(todo_to_delete)
        return True
    
    return False
