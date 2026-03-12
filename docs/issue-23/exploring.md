# EXPLORING - Issue #23

## Issue Summary
The user wants to create a new JavaScript file, `webapp/static/app.js`, to provide frontend interactivity for a ToDo list. This script will fetch data from, add data to, and delete data from a `/api/todos` backend endpoint using vanilla JavaScript and the `fetch` API. A new Python test file, `tests/test_js.py`, should also be created to verify the contents of the JavaScript file.

## Relevant Files
| File Path | Description |
| :--- | :--- |
| `webapp/static/app.js` | **To be created.** This file will contain the core vanilla JavaScript logic for fetching, adding, and deleting ToDo items, and for handling user events. |
| `tests/test_js.py` | **To be created.** This file will contain a simple Python test to read `app.js` and ensure it contains required keywords and function names as specified in the issue. |
| `index.html` | The HTML file that the new `app.js` script will interact with. It is expected to contain elements with IDs `#todo-list`, `#todo-input`, and `#add-btn`. |

## Existing Patterns
- **Directory Structure:** The repository has a `tests/` directory for all test files. The new test file `test_js.py` should be placed there. The web application code is expected to reside in a new `webapp/` directory.
- **Testing:** The `tests/` directory contains Python-based tests using `unittest.mock`. The new test will be a simple file-reading check, which fits within the Python testing ecosystem already in place.
- **Naming Conventions:** Python files use `snake_case.py`. The requested JavaScript functions use `camelCase` (e.g., `loadTodos`). Test files are prefixed with `test_`.
- **API Interaction:** The frontend is expected to interact with a JSON-based REST API at the `/api/todos` path. The JavaScript will use the standard `fetch` API for this.

## Dependencies
- **Browser APIs:** The JavaScript implementation relies solely on standard browser features, specifically the `fetch` API and DOM manipulation methods.
- **Internal Backend API:** The functionality depends on a backend that exposes the following endpoints, though this backend is not present in the provided file tree:
    - `GET /api/todos`
    - `POST /api/todos`
    - `DELETE /api/todos/{id}`

## Observations
- The directories `webapp/` and `webapp/static/` do not currently exist and will need to be created.
- The backend API that the JavaScript will communicate with is not defined or implemented in the provided codebase. The frontend development will proceed based on the API contract described in the issue.
- The `index.html` file exists at the root, and the JavaScript will be written to manipulate its DOM, assuming the presence of specific elements (`#todo-list`, `#todo-input`, `#add-btn`).
