# RESEARCHING - Issue #4

## Research Findings
### Frontend JavaScript Best Practices
1.  **DOM Manipulation:** For interacting with HTML elements, standard DOM APIs should be used.
    *   `document.querySelector()` or `document.getElementById()` to find elements.
    *   `document.createElement()` to create new elements.
    *   `element.appendChild()` to add elements to the DOM tree.
    *   `element.innerHTML = ''` is a common and simple way to clear container elements.
    *   **Security:** To prevent Cross-Site Scripting (XSS), user-provided content (like a todo title) should always be inserted into the DOM using `element.textContent` or `element.innerText`, not `element.innerHTML`.

2.  **API Communication (`fetch`):** The `fetch` API is the modern standard for making network requests in the browser.
    *   It is promise-based, making it ideal for use with `async/await` syntax for cleaner, more readable asynchronous code.
    *   **POST Requests:** To send JSON data, the request requires `method: 'POST'`, `headers: { 'Content-Type': 'application/json' }`, and a `body` that is a JSON string (`JSON.stringify(payload)`).
    *   **DELETE Requests:** These are simpler and just require `method: 'DELETE'`.
    *   **Error Handling:** A `fetch` call only rejects on network errors. HTTP error statuses (like 404 or 500) do not cause the promise to reject. It is essential to check the `response.ok` property (which is `true` for statuses 200-299) and handle non-successful responses appropriately. Unhandled promise rejections and other errors should be caught using a `try...catch` block around `await` calls.

3.  **Event Handling:**
    *   **Page Load:** The `DOMContentLoaded` event is the standard and most reliable way to ensure the DOM is fully parsed before running any JavaScript that manipulates it. The script should be wrapped in a listener for this event: `document.addEventListener('DOMContentLoaded', () => { ... });`.
    *   **Element Events:** Using `element.addEventListener('click', handler)` is the modern best practice. It separates concerns (HTML structure from JS behavior) and allows multiple listeners on one element. The issue explicitly requests using an `onclick` HTML attribute for delete buttons. While less ideal than using event delegation, it is feasible for this simple case. This involves embedding the function call directly in the HTML string, e.g., `<button onclick="deleteTodo(${todo.id})">X</button>`.

### Python Testing
The request for `tests/test_js.py` involves a very basic check. The test will not execute the JavaScript but simply read it as a text file and assert that certain keywords and function names exist. This can be done using Python's standard file I/O and `assert` statements. This pattern is similar to what's seen in `tests/test_duplication_checker.py` and `tests/test_hallucination_checker.py`, which also open and read source files for analysis.

## Duplication Check
The repository consists almost entirely of Python code for a backend system.
*   **No Frontend JavaScript:** There is no existing `webapp` directory, `static` directory, or any `.js` files that perform client-side DOM manipulation or API calls using `fetch`. The requested code will be entirely new.
*   **No Reusable Logic:** The API calls in `dashboard/app.py` and `src/github_client.py` are performed from Python on the server-side, using specific libraries (`pygithub`). This logic is not applicable or reusable for a client-side JavaScript implementation.
*   **Testing Pattern:** The `tests/` directory contains many `test_*.py` files. While the *content* of the new `test_js.py` won't be similar to the existing unit tests (which use `unittest.mock`), the *practice* of creating a dedicated test file in this directory aligns with the project's structure.

Therefore, this task requires creating new files and logic from scratch; no refactoring or extension of existing code is possible.

## Recommended Approach
1.  **File Creation:** Create the directory structure `webapp/static/` and the new file `webapp/static/app.js`. Also create the test file `tests/test_js.py`.

2.  **JavaScript (`app.js`):**
    *   Wrap all code in a `document.addEventListener('DOMContentLoaded', ...)` block to ensure the HTML is ready before the script runs.
    *   Implement `loadTodos()` using `async/await` and `fetch`. It should:
        *   Make a `GET` request to `/api/todos`.
        *   Use a `try...catch` block for error handling (e.g., console logging failures).
        *   Check `response.ok` before attempting to parse JSON.
        *   Clear the `#todo-list` element using `innerHTML = ''`.
        *   Iterate over the fetched todos. For each todo, create an `<li>` element.
        *   Set the todo's title using `li.textContent` to prevent XSS.
        *   Create a `<button>` element for deletion. Set its `onclick` attribute to call `deleteTodo` with the todo's ID.
        *   Append the text and button to the `<li>`, and the `<li>` to the `#todo-list`.
    *   Implement `addTodo()` using `async/await` and `fetch`. It should:
        *   Read the value from `#todo-input` and `trim()` it.
        *   If the value is not empty, perform a `POST` request to `/api/todos` with the correct headers and a JSON body (`{ "title": value }`).
        *   After the request completes successfully, clear the input field and call `loadTodos()` to refresh the list.
        *   Include `try...catch` for error handling.
    *   Implement `deleteTodo(id)` using `async/await` and `fetch`. It should:
        *   Perform a `DELETE` request to the dynamic URL `/api/todos/${id}`.
        *   After the request completes successfully, call `loadTodos()` to refresh the list.
        *   Include `try...catch` for error handling.
    *   Add event listeners for the static elements:
        *   `document.getElementById('add-btn').addEventListener('click', addTodo);`
        *   `document.getElementById('todo-input').addEventListener('keypress', (e) => { if (e.key === 'Enter') addTodo(); });`

3.  **Python Test (`test_js.py`):**
    *   Define a single test function.
    *   Open and read the contents of `webapp/static/app.js`.
    *   Use multiple `assert 'keyword' in content` statements to verify the presence of `"loadTodos"`, `"addTodo"`, `"deleteTodo"`, `"/api/todos"`, and `"fetch"`.

## Risks and Edge Cases
*   **Missing Backend:** The backend API (`/api/todos`) is not implemented in the repository. All `fetch` calls will fail with 404 errors until the API is created. The JavaScript should handle these errors gracefully by logging them to the console so the UI doesn't break.
*   **CORS Policy:** When a backend is eventually created, if it's served on a different port or domain from the frontend, Cross-Origin Resource Sharing (CORS) issues will arise. The backend will need to be configured to send the appropriate `Access-Control-Allow-Origin` headers.
*   **Data Integrity:** The `loadTodos()` function, as requested, re-renders the entire list on every add/delete operation. This is simple but can cause a UI flicker and is inefficient for large lists. For this issue, this approach is acceptable as it meets the requirements.
*   **Input Handling:** The `addTodo` function should handle empty strings and strings with only whitespace by using `.trim()` before checking the length. The current requirement ("if not empty") implies this.
*   **Security (XSS):** It is critical to use `element.textContent` when inserting the todo title into the `<li>`. Using `innerHTML` would create a security vulnerability.
*   **Global Functions:** The `deleteTodo` function will be attached to the global `window` object because of the `onclick` attribute. This pollutes the global namespace but is a direct consequence of the requirement.

## Sources
*   MDN Web Docs - Using the Fetch API: [https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
*   MDN Web Docs - Document: DOMContentLoaded event: [https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event](https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event)
*   MDN Web Docs - Document.createElement(): [https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement](https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement)
*   MDN Web Docs - Node.textContent: [https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)
*   OWASP - Cross-Site Scripting (XSS) Prevention Cheat Sheet: [https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
