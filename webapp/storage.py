from .models import Todo

# In-memory storage components
todos: list[dict] = []
_next_id: int = 1


def add_todo(title: str) -> dict:
    """
    Creates a new todo with an auto-incremented ID and current timestamp,
    adds it to the in-memory list, and returns the created todo as a dictionary.

    Args:
        title: The title of the todo.

    Returns:
        A dictionary representing the new todo.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    _next_id += 1
    return todo_dict


def list_todos() -> list[dict]:
    """
    Returns a copy of the list of all todo items.

    Returns:
        A list of dictionaries, where each dictionary is a todo.
    """
    return todos.copy()


def delete_todo(todo_id: int) -> bool:
    """
    Removes a todo from the list based on its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was found and removed, False otherwise.
    """
    initial_count = len(todos)
    # Rebuild the list, excluding the todo with the matching ID.
    # Modifying the list in-place to avoid 'global' keyword.
    todos[:] = [todo for todo in todos if todo.get("id") != todo_id]
    return len(todos) < initial_count
