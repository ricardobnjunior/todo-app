# PLANNING - Issue #4

## Architecture
The solution will introduce a new client-side component to the project. It involves creating a new directory structure, `webapp/static/`, to house the frontend JavaScript file, `app.js`.

The `app.js` file will be written in vanilla JavaScript and will be responsible for all client-side interactivity of a To-Do list application. Its core responsibilities are:
1.  **Fetching and Rendering Data**: On page load, it will fetch the list of todos from a backend API endpoint (`GET /api/todos`) and dynamically render them as list items in the HTML.
2.  **Adding Data**: It will handle user input to add new todos. This involves reading from an input field and sending the data to the API via a `POST` request.
3.  **Deleting Data**: It will provide a mechanism to delete todos by sending a `DELETE` request to the API.

The entire script's execution will be deferred until the DOM is fully loaded by using a `DOMContentLoaded` event listener. The functions will use the `fetch` API for network requests and standard DOM manipulation methods. Error handling will be included for API calls to prevent the UI from breaking, especially since the backend API is not yet implemented.

A new test file, `tests/test_js.py`, will be created to perform a basic static check on the generated JavaScript file. This test will not execute the JavaScript but will verify the presence of key function names and strings to ensure the implementation adheres to the requirements.

## Files to Create

### `webapp/static/app.js`
- **Description**: This file will contain all the client-side JavaScript logic for the ToDo list application.
- **Contents**:
  - A `DOMContentLoaded` event listener that wraps the entire script.
  - **`loadTodos()` function**: Fetches all todos from `/api/todos` and renders them into the `#todo-list` UL element.
  - **`addTodo()` function**: Reads the value from `#todo-input`, sends it to `/api/todos` via a POST request, and refreshes the list.
  - **`deleteTodo(id)` function**: Sends a DELETE request to `/api/todos/{id}` and refreshes the list. This function will be attached to the `window` object to be accessible from `onclick` attributes.
  - Event listener setup for the add button (`#add-btn`) and the input field (`#todo-input`) for 'Enter' keypresses.

### `tests/test_js.py`
- **Description**: A Python test file to perform a basic static check on `app.js`.
- **Contents**:
  - A single test function, `test_app_js_content`.
  - This test will open `webapp/static/app.js`, read its content, and assert that the required keywords (`loadTodos`, `addTodo`, `deleteTodo`, `/api/todos`, `fetch`) are present in the file as strings.

## Files to Modify
No files will be modified. This issue only involves the creation of new files.

## TODO List
1.  Create the directory structure `webapp/static/`. - [simple]
2.  Create the empty file `webapp/static/app.js`. - [simple]
3.  In `app.js`, set up the main `DOMContentLoaded` event listener to wrap all subsequent code. - [simple]
4.  Implement the `loadTodos` function inside the listener. This function will fetch `GET /api/todos`, clear the `#todo-list`, and render each todo as an `<li>` with a title and a delete button. Use `textContent` for security. - [medium]
5.  Implement the `addTodo` function inside the listener. This function will read the `#todo-input` value, send a `POST` request to `/api/todos`, clear the input, and call `loadTodos`. - [medium]
6.  Implement the `deleteTodo` function. It will take an `id`, send a `DELETE` request to `/api/todos/{id}`, and call `loadTodos`. Assign this function to `window.deleteTodo` to make it globally accessible for `onclick` attributes. - [simple]
7.  Inside the `DOMContentLoaded` listener, add event listeners for the `#add-btn` click and `#todo-input` keypress (for 'Enter') events, both calling `addTodo`. - [simple]
8.  Add an initial call to `loadTodos()` inside the `DOMContentLoaded` listener to load data when the page first loads. - [simple]
9.  Create the empty test file `tests/test_js.py`. - [simple]
10. Implement the test `test_app_js_content` in `tests/test_js.py`. It will read `webapp/static/app.js` and assert that the strings "loadTodos", "addTodo", "deleteTodo", "/api/todos", and "fetch" are present. - [simple]

## Test Plan
- **Unit Test (Python)**:
  - The test `tests/test_js.py` will verify the static content of the `webapp/static/app.js` file.
  - It will check for the existence of the following substrings:
    - `"function loadTodos"` or `"const loadTodos"`
    - `"function addTodo"` or `"const addTodo"`
    - `"function deleteTodo"` or `"window.deleteTodo"`
    - `"/api/todos"`
    - `"fetch"`
- **Manual End-to-End Test (requires `index.html` and a mock API server)**:
  - Open `index.html` in a browser.
  - **Verify `loadTodos()`**: The page should attempt to fetch todos. In the browser's developer console, a network request to `/api/todos` should be visible. If the API is not running, a 404 error should be logged to the console without crashing the script.
  - **Verify `addTodo()`**:
    - Type a new todo title into the input box and click the "Add" button. A `POST` request to `/api/todos` with the correct JSON body should be sent.
    - Type another todo and press "Enter". The same `POST` request should be sent.
    - The input box should clear after each successful addition.
  - **Verify `deleteTodo()`**:
    - Once todos are rendered (possibly with a mock API), clicking the "X" button next to a todo should trigger a `DELETE` request to `/api/todos/{id}` with the correct ID.
    - After any add or delete operation, the `loadTodos()` function should be called again, triggering a refresh of the list.
