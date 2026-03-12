# PLANNING - Issue #4

## Architecture
The solution involves creating a new frontend component using vanilla JavaScript, which will be served statically. This component will interact with a-yet-to-be-defined backend API to provide a dynamic ToDo list interface. The new JavaScript file will live in a new directory structure, `webapp/static/`, to separate frontend assets from the existing Python-based agent tooling.

The core of the architecture is the `webapp/static/app.js` file. This script will contain three main functions (`loadTodos`, `addTodo`, `deleteTodo`) that encapsulate the logic for fetching data, adding new items, and deleting existing items. It will use the browser's `fetch` API for all communication with the `/api/todos` backend endpoints. DOM manipulation will be used to render the ToDo list dynamically based on the API responses.

A corresponding test file, `tests/test_js.py`, will be added to the existing `tests/` directory. This test will not execute the JavaScript but will perform a static check on the file's contents to ensure that key function names and API paths are present, as per the issue requirements. This provides a basic level of validation within the existing Python test framework.

## Files to Create
*   `webapp/static/app.js`
    *   This file will contain all the client-side JavaScript logic for the ToDo application. It will define functions for loading, adding, and deleting todos, and set up event listeners to make the user interface interactive.

*   `tests/test_js.py`
    *   This file will contain a Python test function using pytest. The test will read the content of `webapp/static/app.js` and verify the presence of specific keywords to ensure the implementation meets the basic requirements.

## Files to Modify
*This issue only requires the creation of new files. No existing files will be modified.*

## TODO List
1.  **Create directory structure**: Create the `webapp/` directory and its subdirectory `static/`. - [simple]
2.  **Create `app.js` and setup DOMContentLoaded listener**: Create the file `webapp/static/app.js`. Add an event listener for `DOMContentLoaded` which will serve as the entry point for the script. Inside this listener, set up event handlers for the `#add-btn` click and `#todo-input` keypress events, and make the initial call to `loadTodos()`. - [simple]
3.  **Implement `loadTodos()` function in `app.js`**: Define the `loadTodos` function. This function will use `fetch` to make a `GET` request to `/api/todos`. Upon receiving the data, it will clear the existing content of the `#todo-list` element. Then, it will iterate through the returned todo items, dynamically creating an `<li>` element for each one. Each `<li>` will contain the todo's title text and a delete button with an `onclick` attribute calling `deleteTodo()` with the item's ID. - [medium]
4.  **Implement `addTodo()` function in `app.js`**: Define the `addTodo` function. It will read the value from the `#todo-input` element. If the value is not empty, it will use `fetch` to send a `POST` request to `/api/todos` with the `title` in the JSON body. After the request is complete, it will clear the input field and call `loadTodos()` to refresh the list. - [medium]
5.  **Implement `deleteTodo()` function in `app.js`**: Define the `deleteTodo(id)` function. It will use `fetch` to send a `DELETE` request to the `/api/todos/{id}` endpoint. After the request completes, it will call `loadTodos()` to refresh the list. This function needs to be globally accessible for the `onclick` attribute to work, so it should be attached to the `window` object. - [simple]
6.  **Create `tests/test_js.py`**: Create the test file in the `tests/` directory. - [simple]
7.  **Implement static test for `app.js`**: In `tests/test_js.py`, write a test function that opens `webapp/static/app.js`, reads its contents, and asserts that the required strings ("loadTodos", "addTodo", "deleteTodo", "/api/todos", "fetch") are all present in the file's content. - [simple]

## Test Plan
1.  **Static JavaScript Test (`tests/test_js.py`)**
    *   **What to test**: The presence of required keywords in `webapp/static/app.js`.
    *   **How to test**: Run the pytest suite. The test will read the content of `app.js` and use `assert "keyword" in content` for each of the required strings: "loadTodos", "addTodo", "deleteTodo", "/api/todos", and "fetch".
    *   **Expected result**: The test passes, confirming the implementation file contains the expected function names and API interactions.

2.  **Manual Functional Test (in-browser)**
    *   **Prerequisites**: A web server serving the `index.html` file and a mock or real backend that responds to the API calls on `/api/todos`.
    *   **What to test**: The full user-facing functionality of the ToDo list.
    *   **How to test**:
        *   **Load**: Open the `index.html` page and verify that an API call to `GET /api/todos` is made and the list is rendered correctly.
        *   **Add**: Type a new todo title into the input field and click "Add". Verify a `POST` request is sent, the input is cleared, and the list refreshes to show the new item.
        *   **Add with Enter**: Repeat the "Add" test but press the Enter key instead of clicking the button.
        *   **Delete**: Click the "X" button next to a todo item. Verify a `DELETE` request is sent for the correct ID and the list refreshes with the item removed.
        *   **Empty Add**: Try to add a todo with no text. Verify no API call is made and the list remains unchanged.
    *   **Expected result**: The UI behaves as expected for all actions, and the correct API requests are made.
