# RESEARCHING - Issue #4

## Research Findings
### Vanilla JavaScript for Frontend Development

The task requires creating a frontend application using only vanilla JavaScript, communicating with a REST API. The standard and modern approach for this involves several key browser APIs:

1.  **DOM Manipulation**: To render the todo list, we will need to interact with the Document Object Model (DOM). Key methods include:
    *   `document.getElementById()` or `document.querySelector()` to find elements in the HTML (e.g., the list `<ul>`, the input field, the add button).
    *   `document.createElement()` to create new elements (e.g., `<li>` for each todo item, `<button>` for delete).
    *   `element.appendChild()` to add a newly created element to the DOM.
    *   `element.textContent = ...` to safely set the text content of an element, preventing Cross-Site Scripting (XSS) vulnerabilities. This is preferable to using `innerHTML` when dealing with user-provided data.
    *   `listElement.innerHTML = ''` is a quick and effective way to clear all child elements from a list before re-rendering.

2.  **Event Handling**: To make the UI interactive, we need to listen for user actions.
    *   `element.addEventListener('event', handlerFunction)` is the modern standard. It allows for a clean separation of concerns (HTML for structure, JS for behavior) and supports adding multiple listeners for the same event.
    *   The issue specifies using the `onclick` HTML attribute for delete buttons. While functional, `addEventListener` is generally considered a better practice. For this task, we will follow the explicit requirement.
    *   The `DOMContentLoaded` event is the correct event to listen for to ensure the DOM is fully loaded before trying to manipulate it or attach listeners.

3.  **Fetch API**: This is the modern standard for making network requests in the browser. It is promise-based, which simplifies handling asynchronous operations.
    *   **GET**: `fetch('/api/todos')` makes a simple GET request. The response needs to be processed with `.then(res => res.json())` to parse the JSON body.
    *   **POST**: Requires an options object: `{ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title: 'New Todo' }) }`.
    *   **DELETE**: Is similar, but simpler: `{ method: 'DELETE' }`.
    *   **Async/Await**: Using `async/await` syntax can make the code more readable and easier to reason about than long `.then()` chains. For example: `async function loadTodos() { try { const response = await fetch(...); const data = await response.json(); ... } catch (error) { console.error('Failed to load todos:', error); } }`. This also provides a natural structure for error handling with `try...catch`.

### Python for Testing
The test requirement is to create a Python script that reads the generated JavaScript file and checks for the presence of certain keywords. This is a simple static check, not a functional test. Python's built-in file I/O (`with open(...) as f:`) is sufficient for this purpose. Assertions (`assert 'keyword' in content`) can be used to perform the checks.

## Duplication Check
The repository contains no existing JavaScript files (`.js`). The codebase is almost exclusively Python, focused on the AI agent's orchestration, with a single `index.html` file at the root. Therefore, there is no existing code to reuse or refactor for this task. The directory `webapp/static/` will be a new addition to the project structure. The testing pattern in `tests/` exists for Python code but this new test `tests/test_js.py` will be the first of its kind for a non-Python file.

## Recommended Approach
1.  **Create Directory Structure**: First, create the `webapp/static/` directories.
2.  **JavaScript File (`app.js`)**:
    *   Wrap the main logic in a `DOMContentLoaded` event listener to ensure the script runs only after the page's HTML is ready.
    *   Implement `loadTodos`, `addTodo`, and `deleteTodo` as separate functions for modularity.
    *   Use `async/await` with `try...catch` blocks for all `fetch` calls. This improves readability and provides robust error handling.
    *   In `loadTodos`, dynamically create `<li>` and `<button>` elements. Set the text using `element.textContent` to prevent XSS. Attach the `deleteTodo(id)` call to the button's `onclick` attribute as requested.
    *   In `addTodo`, perform the check for non-empty input by trimming the value (`.trim()`) to prevent submitting whitespace-only todos.
    *   Attach event listeners for the add button's click and the input field's 'keypress' event within the main `DOMContentLoaded` listener. Check for `event.key === 'Enter'` in the keypress handler.
3.  **Test File (`test_js.py`)**:
    *   Create a simple Python test file in the `tests/` directory.
    *   It should define a test function that opens and reads `webapp/static/app.js`.
    *   Use `assert "keyword" in file_content` to verify the presence of "loadTodos", "addTodo", "deleteTodo", "/api/todos", and "fetch" as required.

This approach fulfills all requirements while adhering to modern JavaScript best practices for clarity, security, and maintainability.

## Risks and Edge Cases
*   **Backend API Dependency**: The biggest risk is that the frontend code is being developed without an existing backend. The API endpoints (`GET /api/todos`, `POST /api/todos`, `DELETE /api/todos/{id}`) and JSON format (`{"id": ..., "title": ...}`) are assumed. Any deviation in the future backend implementation will break the frontend. This contract must be strictly followed.
*   **Error Handling**: If a `fetch` call fails (e.g., network error, server 5xx error), the application should handle it gracefully. The recommended `try...catch` blocks should at least log the error to the console. A more advanced implementation might show a user-facing error message.
*   **UI State/Flickering**: The specified logic of re-calling `loadTodos()` after every add/delete operation is simple but can cause a noticeable flicker as the entire list is cleared and re-rendered. For this small application, it's acceptable. For a larger one, optimistic UI updates (modifying the DOM directly before the API call completes) would provide a better user experience.
*   **HTML Structure Dependency**: The JavaScript code assumes specific `id` attributes (`#todo-list`, `#todo-input`, `#add-btn`) exist in the `index.html`. If these are changed in the HTML, the JavaScript will fail.

## Sources
*   [MDN Web Docs: Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
*   [MDN Web Docs: async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
*   [MDN Web Docs: Document: DOMContentLoaded event](https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event)
*   [MDN Web Docs: Introduction to the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)
