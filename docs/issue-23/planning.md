# PLANNING - Issue #23

## Architecture
The solution involves creating a new static JavaScript file to handle the frontend logic for a To-Do application. This file will be self-contained and use vanilla JavaScript to interact with a backend API via the `fetch` API. All logic will be executed after the DOM is fully loaded.

The architecture consists of three main parts:
1.  **DOM Manipulation & Event Handling**: The script will select elements from the `index.html` page by their IDs (`#todo-list`, `#todo-input`, `#add-btn`), listen for user events (clicks, keypresses), and update the DOM dynamically by creating and removing `<li>` elements.
2.  **API Communication Layer**: Three functions (`loadTodos`, `addTodo`, `deleteTodo`) will encapsulate the `fetch` calls to the REST API endpoints (`GET /api/todos`, `POST /api/todos`, `DELETE /api/todos/{id}`). These functions will handle asynchronous network requests and process the responses.
3.  **Static Testing**: A new Python test file will be added to the existing `pytest` suite. This test will not execute the JavaScript but will perform a static check on the file's content to ensure key functions and API paths are present, as a basic form of contract testing.

The new directory `webapp/static/` will be created to house the frontend assets, separating them from the backend Python source code.

## Files to Create

| Path | Description |
| :--- | :--- |
| `webapp/static/app.js` | This file will contain all the client-side JavaScript code. It will define functions to load, add, and delete To-Do items by making API calls. It will also attach event listeners to the HTML elements to make the page interactive. |
| `tests/test_js.py` | This Python test file will verify that `webapp/static/app.js` contains the required function names (`loadTodos`, `addTodo`, `deleteTodo`) and strings (`/api/todos`, `fetch`), ensuring the implementation adheres to the issue's requirements. |

## Files to Modify
No existing files need to be modified for this issue.

## TODO List

| # | Task | Complexity |
| :--- | :--- | :--- |
| 1. | Create the directory structure `webapp/static/`. | simple |
| 2. | Create the `webapp/static/app.js` file. | simple |
| 3. | In `app.js`, add a `DOMContentLoaded` event listener to wrap all the code. | simple |
| 4. | Inside the `DOMContentLoaded` listener, declare the `loadTodos` function. It should fetch `GET /api/todos`, clear the `#todo-list` element, and render the fetched todos as `<li>` elements. Each `<li>` should contain the todo title and a delete button with an `onclick` attribute. | medium |
| 5. | Define the `deleteTodo(id)` function in the global scope so it can be called by `onclick`. This function will make a `DELETE` request to `/api/todos/{id}` and then call `loadTodos()` to refresh the list. | medium |
| 6. | Inside the `DOMContentLoaded` listener, declare the `addTodo` function. It should read from `#todo-input`, perform a `POST` request to `/api/todos` with the title, and upon success, clear the input and call `loadTodos()`. | medium |
| 7. | Inside the `DOMContentLoaded` listener, add an event listener to the `#add-btn` element that calls `addTodo` on `click`. | simple |
| 8. | Inside the `DOMContentLoaded` listener, add an event listener to the `#todo-input` element that calls `addTodo` on a `keypress` event if the key is 'Enter'. | simple |
| 9. | Inside the `DOMContentLoaded` listener, add an initial call to `loadTodos()` to populate the list when the page loads. | simple |
| 10. | Create the `tests/test_js.py` file. | simple |
| 11. | In `tests/test_js.py`, write a test function that opens `webapp/static/app.js`, reads its content, and asserts that the strings "loadTodos", "addTodo", "deleteTodo", "/api/todos", and "fetch" are present. | simple |

## Test Plan

### Static Tests (Automated)
A new test file `tests/test_js.py` will be created to perform static checks on the generated JavaScript code.
-   **`test_app_js_content()`**:
    -   **Verify**: This test will read the content of `webapp/static/app.js`.
    -   **Assert**: It will check for the presence of the following required substrings:
        -   `"loadTodos"`
        -   `"addTodo"`
        -   `"deleteTodo"`
        -   `"/api/todos"`
        -   `"fetch"`

### Manual Functional Tests (To be performed after implementation)
These tests require opening `index.html` in a browser with a working backend API.
-   **Page Load**:
    -   **Action**: Load the `index.html` page.
    -   **Expected**: The `loadTodos()` function is called, and the page displays the current list of todos from the API.
-   **Add Todo**:
    -   **Action**: Type a new todo item into the `#todo-input` field and click the "Add" button or press Enter.
    -   **Expected**: The `addTodo()` function is called, a `POST` request is sent, the input field is cleared, and the list refreshes to show the new item.
-   **Add Empty Todo**:
    -   **Action**: Click the "Add" button or press Enter while the input field is empty.
    -   **Expected**: No API call is made, and the list remains unchanged.
-   **Delete Todo**:
    -   **Action**: Click the "X" button next to an existing todo item.
    -   **Expected**: The `deleteTodo(id)` function is called with the correct ID, a `DELETE` request is sent, and the list refreshes to show the item has been removed.
-   **Error Handling**:
    -   **Action**: Simulate a failed API request (e.g., by stopping the backend server).
    -   **Expected**: Check the browser's developer console for error messages logged by the `fetch`'s `.catch()` block. The UI should not break.
