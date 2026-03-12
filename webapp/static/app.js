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
