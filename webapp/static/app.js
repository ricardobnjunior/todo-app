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
