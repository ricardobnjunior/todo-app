from webapp.models import Todo

# Module-level in-memory storage for todos
# A list of dictionaries, where each dictionary represents a todo.
todos: list[dict] = []

# Module-level counter for the next available todo ID.
_next_id: int = 1

def add_todo(title: str) -> dict:
    """
    Creates a new todo with a unique ID and timestamp, adds it to the
    in-memory list, and returns the new todo as a dictionary.

    Args:
        title: The title of the todo.

    Returns:
        A dictionary representing the newly created todo.
    """
    global _next_id
    new_todo = Todo(id=_next_id, title=title)
    todo_dict = new_todo.model_dump()
    todos.append(todo_dict)
    _next_id += 1
    return todo_dict

def list_todos() -> list[dict]:
    """
    Returns a copy of the list of all todos.

    Returns:
        A list of dictionaries, where each dictionary is a todo.
    """
    return todos[:]

def delete_todo(todo_id: int) -> bool:
    """
    Deletes a todo from the in-memory list based on its ID.

    Args:
        todo_id: The ID of the todo to delete.

    Returns:
        True if a todo was found and deleted, False otherwise.
    """
    global todos
    initial_len = len(todos)
    todos = [todo for todo in todos if todo.get("id") != todo_id]
    return len(todos) < initial_len
