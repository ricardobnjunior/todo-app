# PLANNING - Issue #22

## Architecture
The solution involves adding a new, self-contained frontend component to the project within a new `webapp/` directory. This component will consist of a single static HTML file with embedded CSS. The HTML file will provide the basic structure for a ToDo list application.

The key aspects of the architecture are:
1.  **Directory Structure:** A new `webapp/static/` directory will be created to house the static frontend assets, separating them from the existing Python backend code (`src/`) and dashboard (`dashboard/`). This follows standard web application conventions.
2.  **Frontend Code:** `webapp/static/index.html` will be the entry point for the frontend. It will contain all the necessary HTML for the page structure and all the CSS for styling within a `<style>` tag. This avoids external dependencies and additional file requests for styling. It will reference a JavaScript file, `app.js`, which is planned for a future task.
3.  **Testing:** A new test file, `tests/test_html.py`, will be created to ensure the integrity of the `index.html` file. This test will perform simple static analysis by reading the file and asserting the presence of required element IDs and script references. This maintains the project's practice of having corresponding tests for new features.

This approach is non-intrusive and does not require modifications to any existing backend or application logic.

## Files to Create
- **`webapp/static/index.html`**: The main HTML file for the ToDo application frontend. It will contain the HTML structure, a centered container, a form for adding tasks, an empty list for displaying tasks, and all necessary CSS rules embedded in a `<style>` tag.
- **`tests/test_html.py`**: A new Python test file to validate the contents of `webapp/static/index.html`.

## Files to Modify
None.

## TODO List
1.  **Create directories `webapp/` and `webapp/static/`** - simple
    *   Create the necessary directory structure to house the new frontend assets.

2.  **Create `webapp/static/index.html` with HTML structure** - simple
    *   Set up the basic HTML5 document structure (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`).
    *   Add the page `<title>ToDo List</title>`.
    *   Add a centered `div` container.
    *   Inside the container, add an `<h1>` with "ToDo List".
    *   Add a `<form>` element containing an `<input type="text" id="todo-input">` and a `<button id="add-btn">`.
    *   Add an empty `<ul id="todo-list">`.
    *   Add the `<script src="/static/app.js"></script>` tag before the closing `</body>` tag.

3.  **Embed CSS within a `<style>` tag in `index.html`** - medium
    *   Add a `<style>` tag in the `<head>`.
    *   Style the `body` with the specified background color and font.
    *   Style the main container to have a `max-width` of `600px`, be centered (`margin: auto`), and have a white card appearance (`background: #fff`, `padding`, `box-shadow`, `border-radius`).
    *   Use Flexbox to style the form, making the input field grow to fill available space next to the "Add" button.
    *   Define styles for list items (`li`) within `#todo-list`, using Flexbox to place task text on the left and a placeholder for a delete button on the right.
    *   Add a subtle hover effect for the list items.
    *   Style the placeholder for the delete button (e.g., a class `.delete-btn`) with a red color.

4.  **Create `tests/test_html.py` to validate `index.html`** - simple
    *   Create the new test file `tests/test_html.py`.
    *   Import the `pathlib` module.
    *   Define a test function `test_index_html_content`.
    *   Inside the test, read the content of `webapp/static/index.html`.
    *   Assert that the file content contains the required strings: `id="todo-input"`, `id="add-btn"`, `id="todo-list"`, and `src="/static/app.js"`.

## Test Plan
- **Unit Test for HTML Content (`tests/test_html.py`):**
    -   **Objective:** Verify that the static `index.html` file is created correctly and contains all the required elements and references.
    -   **Setup:** The test will need to locate and read the `webapp/static/index.html` file from the project root. Using `pathlib` is recommended for robust path handling.
    -   **Assertions:**
        1.  Verify the file exists at the correct path.
        2.  Read the file content into a string.
        3.  Assert that the string contains `id="todo-input"` to ensure the task input field is present.
        4.  Assert that the string contains `id="add-btn"` to ensure the add button is present.
        5.  Assert that the string contains `id="todo-list"` to ensure the task list container is present.
        6.  Assert that the string contains `src="/static/app.js"` to ensure the JavaScript file is correctly referenced.
