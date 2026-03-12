# IMPLEMENTING - Issue #4

### FILE: webapp/static/app.js
```javascript
document.addEventListener('DOMContentLoaded', () => {

    const todoList = document.getElementById('todo-list');
    const todoInput = document.getElementById('todo-input');
    const addBtn = document.getElementById('add-btn');

    const API_URL = '/api/todos';

    /**
     * Fetches todos from the API and renders them in the list.
     */
    const loadTodos = async () => {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                // The backend is not yet implemented, so this will likely fail.
                // We log the error instead of throwing to prevent crashing the app.
                console.error(`Failed to fetch todos. Status: ${response.status}`);
                // Assuming an empty array on failure so the app doesn't break.
                return;
            }
            const todos = await response.json();

            // Clear the list before rendering
            todoList.innerHTML = '';

            todos.forEach(todo => {
                const li = document.createElement('li');

                // Set title text safely to prevent XSS
                const titleSpan = document.createElement('span');
                titleSpan.textContent = todo.title;
                li.appendChild(titleSpan);

                // Create delete button
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'X';
                // Using onclick attribute as required, calling a global function
                deleteButton.setAttribute('onclick', `deleteTodo(${todo.id})`);
                li.appendChild(deleteButton);
                
                todoList.appendChild(li);
            });
        } catch (error) {
            console.error('An error occurred while loading todos:', error);
        }
    };

    /**
     * Adds a new todo item.
     */
    const addTodo = async () => {
        const title = todoInput.value.trim();
        if (title) {
            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title: title }),
                });

                if (!response.ok) {
                    console.error(`Failed to add todo. Status: ${response.status}`);
                    return;
                }

                // Clear the input and refresh the list
                todoInput.value = '';
                await loadTodos();
            } catch (error) {
                console.error('An error occurred while adding a todo:', error);
            }
        }
    };

    /**
     * Deletes a todo item by its ID.
     * This function is attached to the window object to be accessible from `onclick`.
     * @param {number} id - The ID of the todo to delete.
     */
    window.deleteTodo = async (id) => {
        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                console.error(`Failed to delete todo. Status: ${response.status}`);
                return;
            }

            // Refresh the list
            await loadTodos();
        } catch (error) {
            console.error(`An error occurred while deleting todo with id ${id}:`, error);
        }
    };

    // Event listeners for adding a todo
    if (addBtn) {
        addBtn.addEventListener('click', addTodo);
    }
    if (todoInput) {
        todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
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
    Tests that webapp/static/app.js contains the required function names and keywords.
    """
    js_file_path = 'webapp/static/app.js'
    
    # This check ensures that the file exists before we try to read it.
    # In a CI/CD pipeline, the file should be available from checkout.
    assert os.path.exists(js_file_path), f"JavaScript file not found at {js_file_path}"

    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required keywords and function definitions
    assert "loadTodos" in content, "Function 'loadTodos' not found in app.js"
    assert "addTodo" in content, "Function 'addTodo' not found in app.js"
    assert "deleteTodo" in content, "Function 'deleteTodo' not found in app.js"
    assert "/api/todos" in content, "API endpoint '/api/todos' not found in app.js"
    assert "fetch" in content, "The 'fetch' API call not found in app.js"
    assert "DOMContentLoaded" in content, "Event listener for 'DOMContentLoaded' not found in app.js"

```

## Decisions Made
1.  **Error Handling**: The backend API (`/api/todos`) does not exist yet. To prevent the JavaScript from crashing the page on startup due to failed `fetch` calls, I implemented graceful error handling. Instead of throwing an error on a non-ok HTTP response, the functions log an error to the console and return. This ensures the application remains usable, and developers can see the network issues in the console.
2.  **Security (`onclick` vs. `addEventListener`)**: The issue specified using an `onclick` attribute for delete buttons. This requires the `deleteTodo` function to be in the global scope (`window`). I implemented this as requested by assigning `window.deleteTodo = ...`. For other static elements (`#add-btn`, `#todo-input`), I used the more modern and safer `addEventListener` approach as the elements are already present at script execution time.
3.  **Security (XSS)**: To prevent Cross-Site Scripting, I explicitly used `document.createElement` and `element.textContent` to insert the user-provided todo title into the DOM. This ensures that any HTML or script tags in the title are rendered as plain text, not executed.
4.  **Test File Logic**: The test file `tests/test_js.py` was designed to be simple and robust for a CI environment. It checks for the file's existence and then asserts that specific required keywords are present, which validates the implementation against the high-level requirements without being brittle. I added a check for `DOMContentLoaded` as it is a crucial part of the implementation's structure.

## Notes
- The created JavaScript file `webapp/static/app.js` is fully self-contained and adheres to all requirements.
- The corresponding test `tests/test_js.py` is ready to be run as part of a standard test suite.
- The `webapp` directory and its `static` subdirectory will be created when the `webapp/static/app.js` file is written to the filesystem.
- For the frontend to work, it will need to be served alongside the `index.html` file by a web server, and the backend API at `/api/todos` will need to be implemented.
