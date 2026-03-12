# RESEARCHING - Issue #23

## Research Findings
Based on the issue requirements, the core of the task is to use vanilla JavaScript to interact with a REST API and manipulate the DOM. The best practices and standard APIs for this are well-established.

1.  **Asynchronous Operations with `fetch`**: The `fetch` API is the modern standard for making network requests in the browser. It is promise-based, which allows for clean handling of asynchronous operations.
    *   **GET**: A simple `fetch('/api/todos')` is used to retrieve data. The response body must be parsed using `response.json()`.
    *   **POST**: To create a resource, the `fetch` call requires a configuration object specifying `method: 'POST'`, `headers: { 'Content-Type': 'application/json' }`, and a `body` containing the JSON-stringified payload (`JSON.stringify(data)`).
    *   **DELETE**: To delete a resource, the configuration object needs `method: 'DELETE'`. The URL should include the ID of the resource to be deleted, like `/api/todos/{id}`.
    *   **Error Handling**: `fetch` only rejects a promise on network failures. It does not reject on HTTP error statuses (like 404 or 500). Best practice is to check the `response.ok` property (which is true for statuses in the 200-299 range) and handle non-ok statuses explicitly. For this task, basic error handling with `.catch()` for network errors will suffice.

2.  **DOM Manipulation**:
    *   **Event Handling**: The modern approach is to use `element.addEventListener('event', callback)`. This separates concerns by keeping JavaScript logic out of the HTML. The issue specifically requests using an `onclick` HTML attribute for delete buttons, which is a simpler but older pattern.
    *   **Element Creation**: Programmatically creating DOM nodes with `document.createElement()`, setting their properties (like `textContent` to prevent XSS vulnerabilities), and appending them with `appendChild()` is the safest and most flexible method.
    *   **Waiting for DOM Ready**: All DOM manipulation logic and event listener attachment should be deferred until the DOM is fully loaded. This is achieved by wrapping the code in a `document.addEventListener('DOMContentLoaded', () => { ... });` block.

3.  **Python Testing**:
    *   The requirement is for a simple static check of the generated JavaScript file, not a functional or end-to-end test.
    *   Standard Python file I/O (`with open(...)`) is sufficient to read the file content.
    *   The `pytest` framework, already in use in the repository, can be used with simple `assert` statements to verify that specific substrings (function names, API paths) exist in the file's content.

## Duplication Check
The repository contains a significant amount of Python code for a backend system related to AI agent orchestration and a dashboard application. However, there is no existing frontend JavaScript code that performs client-side rendering or interacts with a REST API in the manner requested. The `dashboard/` sub-project is a Python web application, but it does not contain any static JavaScript files related to a ToDo application.

Therefore, the requested `webapp/static/app.js` and `tests/test_js.py` files will be entirely new, and there is no existing code to reuse or refactor for this task.

## Recommended Approach
1.  **Create `webapp/static/app.js`**:
    *   Wrap all code in a `document.addEventListener('DOMContentLoaded', ...)` to ensure the script runs only after the HTML document is fully parsed.
    *   **`loadTodos()` function**:
        *   Should first clear the current list content using `todoListElement.innerHTML = '';` to prevent duplication on refresh.
        *   Use `fetch` to make a `GET` request to `/api/todos`.
        *   Process the JSON response and iterate through the array of todo items.
        *   For each item, create a new `<li>` element. To meet the `onclick` requirement, construct the element's HTML as a string: `li.innerHTML = \`${todo.title} <button onclick="deleteTodo(${todo.id})">X</button>\`;`.
        *   Append the new `<li>` to the `#todo-list` element.
    *   **`addTodo()` function**:
        *   Retrieve the text from the `#todo-input` element.
        *   Check if the input is not empty.
        *   Use `fetch` to make a `POST` request to `/api/todos`, sending the `{ "title": "..." }` payload.
        *   Upon successful response, clear the input field and call `loadTodos()` to refresh the list with the newly added item.
    *   **`deleteTodo(id)` function**:
        *   This function will be called from the `onclick` attribute and receive the todo `id`.
        *   Use `fetch` to make a `DELETE` request to `/api/todos/${id}`.
        *   Upon successful response, call `loadTodos()` to refresh the list.
    *   **Event Listeners**: Inside the `DOMContentLoaded` callback:
        *   Attach a `click` listener to `#add-btn` that calls `addTodo()`.
        *   Attach a `keypress` listener to `#todo-input` that checks if the pressed key is "Enter" and calls `addTodo()` if it is.
        *   Make an initial call to `loadTodos()` to populate the list on page load.

2.  **Create `tests/test_js.py`**:
    *   Create a new test file in the `tests/` directory.
    *   Define a test function (e.g., `test_app_js_content`).
    *   In the function, open and read the contents of `webapp/static/app.js`.
    *   Use a series of `assert "keyword" in content` checks to verify the presence of the required strings: `"loadTodos"`, `"addTodo"`, `"deleteTodo"`, `"/api/todos"`, and `"fetch"`.

This approach directly fulfills all requirements of the issue using standard web APIs and aligns with the existing testing structure of the project.

## Risks and Edge Cases
*   **Missing Backend**: The frontend JavaScript will be written against a defined API contract (`GET /api/todos`, etc.). Since this API is not part of the current codebase, the frontend cannot be fully tested end-to-end. The implementation will have to assume the backend will function as specified.
*   **HTML Dependency**: The JavaScript code's correctness depends on an HTML file containing elements with specific IDs (`#todo-list`, `#todo-input`, `#add-btn`). If the `index.html` file is missing or has a different structure, the script will throw errors at runtime.
*   **Cross-Site Scripting (XSS)**: The use of `innerHTML` to set the content of the `<li>` elements introduces a potential XSS vulnerability if a todo `title` contains malicious HTML. While acceptable for this exercise, the safer, modern practice is to use `element.textContent` to set user-provided text and create child elements (like the button) programmatically.
*   **UI Flickering**: Calling `loadTodos()` to re-render the entire list after every add/delete operation is simple but can be inefficient and cause a noticeable flicker with large lists. A more optimized approach would be to surgically add or remove individual `<li>` elements from the DOM. The requested approach is fine for a simple application.
*   **User Feedback on Errors**: The current plan involves logging network or server errors to the console. A production-ready application should provide visible feedback to the user (e.g., an alert or a message on the page) when an API call fails.

## Sources
*   [MDN Web Docs: Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
*   [MDN Web Docs: Document: DOMContentLoaded event](https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event)
*   [MDN Web Docs: Document.createElement()](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement)
*   [MDN Web Docs: Element.innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML)
*   [MDN Web Docs: Node.textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)
