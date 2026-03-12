# PLANNING - Issue #3

## Architecture
The solution introduces a new, self-contained frontend component to the project. This component will reside in a new top-level directory, `webapp`, to isolate it from the existing Python backend (`src`) and dashboard (`dashboard`) code.

The architecture will consist of:
1.  A new `webapp/` directory for the frontend application.
2.  A `webapp/static/` subdirectory to hold static assets.
3.  A single static file, `webapp/static/index.html`, which will contain the full HTML structure, embedded CSS for styling, and a reference to an external JavaScript file. This follows a standard pattern for simple single-page applications.
4.  A new test file, `tests/test_html.py`, which will perform basic validation on the `index.html` file to ensure key elements are present. This test will not parse the HTML but will do simple string-based checks, which is sufficient for the requirements.

This design is simple, modular, and does not affect any existing project code, ensuring a clean separation of concerns.

## Files to Create

-   **`webapp/static/index.html`**:
    -   This file will contain the complete HTML structure for the ToDo List application's user interface.
    -   It will include a `<head>` section with the page title and an embedded `<style>` block for all CSS rules.
    -   The `<body>` will contain the main layout container, a header, a form for adding new tasks, and an empty unordered list for displaying tasks.
    -   A `<script>` tag will be included at the end of the `<body>` to link to `app.js`.

-   **`tests/test_html.py`**:
    -   This file will contain a single `pytest` test function.
    -   The function will be responsible for reading the contents of `webapp/static/index.html` and verifying the presence of specific substrings, confirming that required IDs and script references exist in the markup.

## Files to Modify
No files will be modified. This task only involves the creation of new files and directories.

## TODO List
1.  **Create `webapp` directory**: Create the top-level directory for the frontend application. - [simple]
2.  **Create `webapp/static` directory**: Create the subdirectory for static assets inside `webapp`. - [simple]
3.  **Create `webapp/static/index.html` with HTML boilerplate**: Initialize the file with a standard HTML5 structure (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`). Set the page title to "ToDo List". - [simple]
4.  **Add HTML content to `index.html`**: Add the main container `div`, the `<h1>` header, the `<form>` containing the `<input>` with `id="todo-input"` and the `<button>` with `id="add-btn"`. Add the empty `<ul id="todo-list">`. - [simple]
5.  **Add embedded CSS to `index.html`**: Within a `<style>` tag in the `<head>`, write the CSS to style the page. This includes centering the container, creating the white card effect, styling the form and list items using Flexbox, and adding hover effects as required. - [medium]
6.  **Add script reference to `index.html`**: Add the `<script src="/static/app.js"></script>` tag just before the closing `</body>` tag. - [simple]
7.  **Create `tests/test_html.py`**: Create the new test file in the `tests/` directory. - [simple]
8.  **Implement test function in `test_html.py`**: Write a test function that opens `webapp/static/index.html`, reads its contents, and asserts that the strings `"todo-input"`, `"add-btn"`, `"todo-list"`, and `"app.js"` are present. - [simple]

## Test Plan

-   **Unit Tests (`tests/test_html.py`)**
    -   A test named `test_index_html_contains_required_elements` will be created.
    -   It will read the file `webapp/static/index.html`.
    -   It will assert that the file content contains the substring `id="todo-input"`.
    -   It will assert that the file content contains the substring `id="add-btn"`.
    -   It will assert that the file content contains the substring `id="todo-list"`.
    -   It will assert that the file content contains the substring `src="/static/app.js"`.

-   **Manual Browser Test**
    -   Open `webapp/static/index.html` directly in a web browser.
    -   **Verify**: The page has the title "ToDo List".
    -   **Verify**: The layout consists of a single, centered white box (max-width 600px) on a light gray background.
    -   **Verify**: The header "ToDo List" is displayed as an `h1`.
    -   **Verify**: An input field with the placeholder "Digite uma tarefa..." and a button labeled "Adicionar" are displayed side-by-side.
    -   **Verify**: An empty area for the task list exists below the form.
    -   **Verify**: Opening the browser's developer console shows a 404 (Not Found) error for `app.js`, which is expected behavior for this task.
