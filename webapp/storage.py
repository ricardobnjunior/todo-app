from typing import TypedDict, List
from .models import Todo

# An in-memory storage for todos.
# For a real application, this would be replaced with a database.

class TodoDict(TypedDict):
    """
    A dictionary representation of a Todo item, for type hinting.
    """
    id: int
    title: str
    created_at: str

todos: List[TodoDict] = []
_next_id: int = 1

def add_todo(title: str) -> TodoDict:
    """
    Creates a new todo, adds it to the in-memory list, and returns it.

    Args:
        title: The title of the todo task.

    Returns:
        The newly created todo as a dictionary.
    """
    global _next_id
    new_todo_model = Todo(id=_next_id, title=title)
    new_todo_dict = new_todo_model.model_dump()

    todos.append(new_todo_dict)
    _next_id += 1
    
    return new_todo_dict

def list_todos() -> List[TodoDict]:
    """
    Returns a copy of the list of all todos.

    Returns:
        A list of todo dictionaries.
    """
    return todos.copy()

def delete_todo(todo_id: int) -> bool:
    """
    Deletes a todo by its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was deleted, False otherwise.
    """
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return len(todos) < initial_length
