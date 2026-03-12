# IMPLEMENTING - Issue #4

### FILE: webapp/static/app.js
```javascript
// This script provides the frontend interactivity for the ToDo list application.
// It connects to a backend API to fetch, create, and delete todo items.

document.addEventListener('DOMContentLoaded', () => {
    // Select key DOM elements once the document is loaded.
    const todoInput = document.getElementById('todo-input');
    const addBtn = document.getElementById('add-btn');

    // Attach event listeners for user interactions.
    if (addBtn) {
        addBtn.addEventListener('click', addTodo);
    }

    if (todoInput) {
        todoInput.addEventListener('keypress', (event) => {
            // Allow adding todos by pressing the 'Enter' key.
            if (event.key === 'Enter') {
                addTodo();
            }
        });
    }

    // Perform an initial load of the todo items when the page is ready.
    loadTodos();
});

/**
 * Fetches all todo items from the API and renders them in the list.
 */
async function loadTodos() {
    const todoList = document.getElementById('todo-list');
    if (!todoList) {
        console.error('Element with id "todo-list" not found.');
        return;
    }

    // Clear the list to prevent duplicates on refresh.
    todoList.innerHTML = '';

    try {
        const response = await fetch('/api/todos');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const todos = await response.json();

        // Create and append a list item for each todo.
        todos.forEach(todo => {
            const li = document.createElement('li');

            // The text content of the todo.
            const titleSpan = document.createElement('span');
            titleSpan.textContent = todo.title;

            // The delete button for the todo.
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'X';
            // Per requirements, use an onclick attribute to call deleteTodo.
            deleteBtn.setAttribute('onclick', `deleteTodo(${todo.id})`);

            li.appendChild(titleSpan);
            li.appendChild(deleteBtn);

            todoList.appendChild(li);
        });
    } catch (error) {
        console.error('Failed to load todos:', error);
        todoList.textContent = 'Error: Could not load ToDo items.';
    }
}

/**
 * Reads the todo input, sends a new todo to the API, and refreshes the list.
 */
async function addTodo() {
    const todoInput = document.getElementById('todo-input');
    if (!todoInput) {
        console.error('Element with id "todo-input" not found.');
        return;
    }

    const title = todoInput.value.trim();

    // Only add a todo if the input is not empty.
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

            // Clear the input field and refresh the list to show the new item.
            todoInput.value = '';
            loadTodos();
        } catch (error) {
            console.error('Failed to add todo:', error);
        }
    }
}

/**
 * Deletes a todo item by its ID and refreshes the list.
 * This function is declared at the top level, making it globally accessible
 * for the `onclick` attributes generated in `loadTodos`.
 * @param {number} id - The ID of the todo item to delete.
 */
async function deleteTodo(id) {
    try {
        const response = await fetch(`/api/todos/${id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Refresh the list to reflect the deletion.
        loadTodos();
    } catch (error) {
        console.error(`Failed to delete todo with id ${id}:`, error);
    }
}
```

### FILE: tests/test_js.py
```python
import os


def test_app_js_content():
    """
    Tests that webapp/static/app.js contains the required keywords.
    This is a simple static check to verify the implementation against requirements.
    """
    # Construct a path relative to this test file to be robust
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    js_file_path = os.path.join(project_root, 'webapp', 'static', 'app.js')

    assert os.path.exists(js_file_path), f"File not found: {js_file_path}"

    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    required_keywords = [
        "loadTodos",
        "addTodo",
        "deleteTodo",
        "/api/todos",
        "fetch",
    ]

    for keyword in required_keywords:
        assert keyword in content, f"Keyword '{keyword}' not found in webapp/static/app.js"
```

## Decisions Made
1.  **Global `deleteTodo` Function**: The requirement for delete buttons to use `onclick="deleteTodo(id)"` necessitates that the `deleteTodo` function be available in the global scope. I achieved this by defining it as a top-level `async function` in `app.js`. In a standard, non-module script loaded via `<script>`, top-level function declarations are automatically attached to the `window` object. This is simpler and cleaner than explicitly writing `window.deleteTodo = ...`.
2.  **Error Handling**: The requirements did not specify error handling. I made the decision to include basic error handling using `try...catch` blocks for all `fetch` calls. Errors are logged to the browser's console (`console.error`), which is a reasonable default for this type of application and aids in debugging. In case `loadTodos` fails, a user-friendly message is displayed in the list area.
3.  **Code Safety**: To prevent Cross-Site Scripting (XSS) vulnerabilities, I used `element.textContent` to set the todo item's title instead of `element.innerHTML`.
4.  **UX Improvement**: I used `.trim()` on the input value in `addTodo()` to prevent users from adding todos that consist only of whitespace.
5.  **Test File Pathing**: In `tests/test_js.py`, I constructed an absolute path to `webapp/static/app.js` based on the location of the test file itself. This makes the test more robust and less dependent on the current working directory from which `pytest` is executed.

## Notes
- The created `webapp/static/app.js` file assumes a specific HTML structure exists, namely elements with the IDs `#todo-list`, `#todo-input`, and `#add-btn`.
- This frontend code also depends on a backend API being available at `/api/todos` that supports `GET`, `POST` (with a `{ "title": "..." }` body), and `DELETE /api/todos/{id}`. The API is expected to return a JSON array of objects, where each object has at least `id` and `title` properties. This backend is not part of the current implementation.
- The directory `webapp/static/` is new to the project structure, created as requested to hold frontend assets.
