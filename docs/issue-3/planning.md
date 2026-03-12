# PLANNING - Issue #3

## Architecture
The solution will introduce a new directory, `webapp/`, to house the frontend components of the ToDo application. This follows standard project structure conventions by separating frontend code from the backend Python source in `src/`.

The frontend will consist of a single static `index.html` file located in `webapp/static/`. This file will contain all the necessary HTML structure, as well as embedded CSS within a `<style>` tag for all styling requirements. No external CSS or JavaScript libraries will be used. The page will link to a placeholder `app.js` file, which is not part of this task.

A new test file, `tests/test_html.py`, will be created to validate the static HTML. This test will not parse the HTML but will perform simple string-based checks to ensure the presence of key element IDs and the script tag, as required by the issue. This approach is lightweight and avoids adding new testing dependencies.

## Files to Create
- **`webapp/static/index.html`**: This file will contain the complete HTML structure and embedded CSS for the ToDo application's user interface.
- **`tests/test_html.py`**: A new test file to verify that the `index.html` file contains the required elements.

## Files to Modify
None. This task only involves the creation of new files.

## TODO List
1. **Create `webapp/static/index.html` and add HTML structure** - simple
   - Create the necessary directories: `webapp/` and `webapp/static/`.
   - Add the standard HTML5 boilerplate (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`).
   - Set the page title to "ToDo List".
   - Add the main content elements: a centered container `<div>`, an `<h1>` header, a `<form>`, a text `<input>` with `id="todo-input"`, a `<button>` with `id="add-btn"`, and an empty `<ul>` with `id="todo-list"`.

2. **Add JavaScript reference to `index.html`** - simple
   - Add a `<script>` tag just before the closing `</body>` tag, with its `src` attribute set to `/static/app.js`.

3. **Implement embedded CSS in `index.html`** - medium
   - Add a `<style>` tag inside the `<head>`.
   - Write CSS rules to:
     - Set the body background color and main font.
     - Style the main container as a centered white card with a box-shadow.
     - Use Flexbox to align the text input and button side-by-side within the form.
     - Style a placeholder `li` element to use Flexbox (`justify-content: space-between`) for the task title and a delete button.
     - Add a hover effect for list items.

4. **Create `tests/test_html.py`** - simple
   - Create the new test file in the `tests/` directory.

5. **Implement test to validate `index.html`** - simple
   - In `tests/test_html.py`, create a test function that opens and reads `webapp/static/index.html`.
   - Add assertions to verify that the file content contains the required substrings: `id="todo-input"`, `id="add-btn"`, `id="todo-list"`, and `src="/static/app.js"`.

## Test Plan
- **Unit Test:**
  - Create a test case in `tests/test_html.py`.
  - The test will read the contents of `webapp/static/index.html` into a string.
  - It will then assert that specific substrings are present in the content:
    - `id="todo-input"` to verify the task input field exists.
    - `id="add-btn"` to verify the add button exists.
    - `id="todo-list"` to verify the task list container exists.
    - `src="/static/app.js"` to verify the JavaScript file is correctly referenced.
- **Manual Visual Test:**
  - After implementation, open `webapp/static/index.html` in a web browser.
  - Verify that the layout matches the requirements:
    - The page has the title "ToDo List".
    - A centered white container holds the content.
    - The "ToDo List" `h1` heading is visible.
    - The text input and "Adicionar" button are side-by-side.
    - The list area is initially empty.
    - The overall styling (fonts, colors, spacing) is clean and professional.
