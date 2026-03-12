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
