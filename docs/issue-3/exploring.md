# EXPLORING - Issue #3

## Issue Summary
The task is to create a new static HTML file, `webapp/static/index.html`, for a ToDo list application frontend. This includes a specific HTML structure with element IDs, embedded CSS for styling, a reference to a yet-to-be-created `app.js` file, and a new test file, `tests/test_html.py`, to verify the HTML's content.

## Relevant Files
*   **`webapp/static/index.html` (New File)**: This is the main file to be created. It will contain the HTML structure and embedded CSS for the ToDo list user interface. The `webapp` and `webapp/static` directories will need to be created.
*   **`tests/test_html.py` (New File)**: This test file needs to be created to verify that the generated `index.html` contains the required element IDs and the script reference.
*   **`tests/` (Existing Directory)**: This directory will house the new `test_html.py` file. Its existing contents show a pattern of using `pytest` and file-based tests.
*   **`index.html` (Existing File)**: There is an existing `index.html` file in the project root. This file seems to be related to project documentation or overviews and is distinct from the `webapp/static/index.html` file required by this task.

## Existing Patterns
*   **Project Structure**: The project is organized with application logic in `src/`, a dashboard in `dashboard/`, and tests in `tests/`. This task will introduce a new top-level directory, `webapp/`, for the frontend application.
*   **Testing Convention**: The `tests/` directory contains files named `test_*.py`. The new test file should follow this convention. Existing tests appear to use standard Python testing libraries, which will be sufficient for the required file content checks.
*   **Naming Convention**: The issue specifies HTML `id` attributes in kebab-case (`todo-input`, `add-btn`, `todo-list`).

## Dependencies
*   The issue explicitly forbids the use of any external CSS libraries for styling the `index.html` page.
*   The new test file `tests/test_html.py` will depend only on Python's standard library for file I/O and string searching.

## Observations
*   The task introduces a new, previously non-existent component (`webapp`) to the project.
*   The functionality of the ToDo list app seems distinct from the existing AI agent orchestration logic found in the `src/` directory.
*   The `index.html` file will reference `/static/app.js`, but this JavaScript file is not part of the current task and will not exist, resulting in a broken link until it is created in a future step.
*   Care must be taken to create the new `index.html` inside `webapp/static/` and not overwrite the existing `index.html` in the project root.
