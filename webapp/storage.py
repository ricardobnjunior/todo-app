from typing import Optional, Dict, List

# In-memory data store for todos
_todos: Dict[int, Dict] = {}
_next_id = 1

def reset_storage():
    """Resets the in-memory storage. Used for testing."""
    global _todos, _next_id
    _todos = {}
    _next_id = 1

def get_all_todos() -> List[Dict]:
    """Returns a list of all todo items."""
    return list(_todos.values())

def add_todo(title: str) -> Dict:
    """Adds a new todo item to the store."""
    global _next_id
    new_todo = {
        "id": _next_id,
        "title": title
    }
    _todos[_next_id] = new_todo
    _next_id += 1
    return new_todo

def delete_todo(todo_id: int) -> Optional[Dict]:
    """Deletes a todo item by its ID."""
    if todo_id in _todos:
        return _todos.pop(todo_id)
    return None
