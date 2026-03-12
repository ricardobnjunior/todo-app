# IMPLEMENTING - Issue #23

An AI agent in IMPLEMENTING mode.

### FILE: webapp/static/app.js
```javascript
/**
 * Fetches todos from the API and renders them in the list.
 */
async function loadTodos() {
    try {
        const response = await fetch('/api/todos');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const todos = await response.json();
        const todoList = document.getElementById('todo-list');

        // Clear the list before rendering
        todoList.innerHTML = '';

        todos.forEach(todo => {
            const li = document.createElement('li');
            // Note: In a production app, user-generated content like `todo.title`
            // should be sanitized to prevent XSS attacks. For this exercise,
            // we are directly inserting it as requested.
            li.innerHTML = `${todo.title} <button onclick="deleteTodo(${todo.id})">X</button>`;
            li.dataset.id = todo.id;
            todoList.appendChild(li);
        });
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

/**
 * Adds a new todo item.
 */
async function addTodo() {
    const todoInput = document.getElementById('todo-input');
    const title = todoInput.value.trim();

    if (title) {
        try {
            const response = await fetch('/api/todos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: title }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Clear the input and refresh the list
            todoInput.value = '';
            loadTodos();
        } catch (error) {
            console.error('Error adding todo:', error);
        }
    }
}

/**
 * Deletes a todo item by its ID.
 * @param {number} id - The ID of the todo to delete.
 */
async function deleteTodo(id) {
    try {
        const response = await fetch(`/api/todos/${id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Refresh the list to show the item has been removed
        loadTodos();
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}


// Main execution block after the DOM is fully loaded.
document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add-btn');
    const todoInput = document.getElementById('todo-input');

    // Attach event listeners
    if (addBtn) {
        addBtn.addEventListener('click', addTodo);
    }

    if (todoInput) {
        todoInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                addTodo();
            }
        });
    }

    // Initial load of todos
    loadTodos();
});
```

### FILE: tests/test_js.py
```python
import os

def test_app_js_content():
    """
    Tests that the app.js file contains the required function names and keywords.
    """
    # Define the path to the JavaScript file relative to the project root
    js_file_path = os.path.join('webapp', 'static', 'app.js')

    # Ensure the file exists before trying to open it
    assert os.path.exists(js_file_path), f"JavaScript file not found at: {js_file_path}"

    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for the presence of the required substrings as per the issue requirements
    required_strings = [
        "loadTodos",
        "addTodo",
        "deleteTodo",
        "/api/todos",
        "fetch"
    ]

    for required_string in required_strings:
        assert required_string in content, f"Missing required string '{required_string}' in app.js"

```

## Decisions Made
1.  **Function Scope:** All three core functions (`loadTodos`, `addTodo`, `deleteTodo`) were placed in the global scope. This was the simplest way to ensure that `deleteTodo` is accessible from the `onclick` HTML attribute, and it allows `addTodo` and `deleteTodo` to easily call `loadTodos` to refresh the list without complex scope management.
2.  **Asynchronous Syntax:** I used `async/await` syntax for handling `fetch` promises, as it is modern, cleaner, and more readable than `.then()` chaining.
3.  **Error Handling:** Basic error handling was added using `try...catch` blocks for all API calls. Errors are logged to the console, which is a reasonable default for this type of application.
4.  **Security (XSS):** The requirement to use `innerHTML` to construct list items was followed directly. A comment was added to the code noting that in a real-world application, user-provided content like `todo.title` should be sanitized or set via `textContent` to prevent Cross-Site Scripting (XSS) vulnerabilities.
5.  **Test File Path:** The test `tests/test_js.py` assumes it will be run from the project root directory, making `webapp/static/app.js` the correct relative path to the JavaScript file. This aligns with standard `pytest` execution behavior.
6.  **Test Specificity:** The test performs simple substring checks as specified in the issue requirements, rather than more complex parsing or Abstract Syntax Tree analysis, to keep it simple and directly meet the stated goal.

## Notes
- The `webapp/` and `webapp/static/` directories did not exist and will be created as part of the file writing process.
- The functionality of the JavaScript code is dependent on a backend API at `/api/todos` that is not part of this implementation. Manual testing requires a mock or real backend server that implements the `GET /api/todos`, `POST /api/todos`, and `DELETE /api/todos/{id}` endpoints.
- The code also depends on an `index.html` file in the root directory containing elements with IDs `#todo-list`, `#todo-input`, and `#add-btn`.
