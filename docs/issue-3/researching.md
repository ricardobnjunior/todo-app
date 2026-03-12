# RESEARCHING - Issue #3

## Research Findings
### HTML & CSS Best Practices
1.  **HTML Structure**: For the requested layout, standard HTML5 semantic elements are appropriate. The structure should include a `<!DOCTYPE html>` declaration, `<html>`, `<head>`, and `<body>` tags. The `<head>` should contain metadata like `<meta charset="UTF-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1.0">` for responsiveness, and the `<title>`. The main content can be wrapped in a `<main>` or `<div>` tag for styling.

2.  **CSS Layout**:
    *   **Flexbox** is the modern standard for laying out items in a single dimension, making it ideal for this task.
    *   **Centering a Container**: To center the main container both vertically and horizontally, applying `display: flex`, `justify-content: center`, and `align-items: center` to the `<body>` element (with `min-height: 100vh`) is a robust method. A simpler horizontal-only centering can be achieved with `margin: 0 auto;` on the container itself.
    *   **Input and Button**: Placing the text input and button side-by-side can be easily done by wrapping them in a `div` and setting its `display` to `flex`. The input field can be made to fill the available space using `flex-grow: 1`.
    *   **List Items**: The layout for each task (title on the left, 'X' button on the right) is a perfect use case for `display: flex` with `justify-content: space-between` on the `<li>` elements.

3.  **CSS Styling**:
    *   **Embedded CSS**: Placing CSS in a `<style>` tag within the `<head>` is appropriate for small, single-file pages as requested. For larger applications, external stylesheets are generally preferred for caching and maintainability.
    *   **Card Look**: This effect is typically achieved using `background-color: #fff;`, `padding`, `border-radius`, and a subtle `box-shadow`.
    *   **System Fonts**: The `system-ui` font stack (`font-family: system-ui, sans-serif;`) is a good, modern choice that uses the native OS font without requiring web font downloads.

4.  **JavaScript Inclusion**: Placing the `<script>` tag just before the closing `</body>` tag is a long-standing best practice. It ensures the HTML Document Object Model (DOM) is fully parsed and available to the script when it executes, preventing errors from scripts trying to access elements that haven't been loaded yet. Using the `defer` attribute on a script in the `<head>` is a more modern alternative that is non-blocking and executes after the DOM is ready.

### Python Testing
1.  **Testing Static Files**: The task requires verifying the presence of specific substrings within the generated HTML file.
2.  **Simple Substring Check**: The most direct method is to read the entire file into a string and use Python's `in` operator to check for the required substrings (e.g., `'id="todo-input"' in file_content`). This is simple and has no external dependencies.
3.  **HTML Parsing (More Robust)**: A more resilient approach would be to use a library like `BeautifulSoup` to parse the HTML. This allows for querying elements by ID or class (e.g., `soup.find(id='todo-input')`). This method is not affected by whitespace changes or attribute order. However, it would introduce a new testing dependency (`beautifulsoup4`) which is not currently present in the project. Given the simplicity of the requirement, a substring check is sufficient and avoids adding dependencies.

## Duplication Check
*   **HTML/CSS**: The repository contains `index.html` at the root and `escopo/system-overview.html`. These appear to be a placeholder and a generated documentation file, respectively. They do not contain any relevant application structure or styling that can be reused. The `dashboard/` directory contains a Python application but no HTML templates. Therefore, the requested `webapp/static/index.html` will be a completely new file with unique content and styling.
*   **Testing**: The `tests/` directory contains many test files. Some, like `tests/test_duplication_checker.py`, demonstrate file I/O operations within tests. However, these are for creating temporary files for a test run. There are no existing tests that read and validate the content of a static project file like HTML. The testing logic for `tests/test_html.py` will be new.

## Recommended Approach
1.  **File Creation**:
    *   Create the directory structure `webapp/static/`.
    *   Create the new file `webapp/static/index.html`.

2.  **HTML Structure (`index.html`)**:
    *   Start with a standard HTML5 boilerplate.
    *   Set the page title to "ToDo List".
    *   In the `<body>`, create a main container `div` and center it using CSS.
    *   Inside the container, add an `<h1>` heading "ToDo List".
    *   Create a `<form>` element containing a `div` with `display: flex`.
    *   Inside this flex `div`, place the `<input type="text" id="todo-input" ...>` and the `<button id="add-btn">...`.
    *   Below the form, add an empty `<ul id="todo-list">`.
    *   Before the closing `</body>` tag, add `<script src="/static/app.js"></script>`.

3.  **Embedded CSS (`<style>` tag in `<head>`)**:
    *   `body`: Set `background-color: #f5f5f5`, `font-family: system-ui, sans-serif`, and use Flexbox to center the main container.
    *   `.container`: Set `max-width: 600px`, `margin: 20px auto`, `background: #fff`, `padding`, `border-radius`, and `box-shadow`.
    *   `form > div`: Set `display: flex;`.
    *   `#todo-input`: Set `flex-grow: 1;` and apply styling for border, padding, and font size.
    *   `#add-btn`: Style the button with padding, background color, and no border.
    *   `#todo-list`: Remove default list styling (`list-style: none; padding: 0;`).
    *   `#todo-list li`: Define the style for future list items. Use `display: flex`, `justify-content: space-between`, `align-items: center`, and add padding and a bottom border. Define a `:hover` pseudo-class for a background color change.
    *   `.delete-btn`: Define a style for the 'X' button within list items, including `color: red`, `background: none`, `border: none`, and `cursor: pointer`.

4.  **Test Implementation (`tests/test_html.py`)**:
    *   Create the new file `tests/test_html.py`.
    *   Define a test function, `test_index_html_contains_elements`.
    *   Inside the function, construct the path to `webapp/static/index.html`.
    *   Read the entire content of the file into a string variable.
    *   Use `assert 'id="todo-input"' in content` and similar simple string assertions for `"add-btn"`, `"todo-list"`, and `src="/static/app.js"`. This directly satisfies the issue requirements without adding new dependencies.

## Risks and Edge Cases
*   **File Paths**: The test file in `tests/` must correctly locate the HTML file in `webapp/static/`. Using a path relative to the project root is the most reliable way to avoid issues with the test execution directory.
*   **Directory Creation**: The new directories `webapp` and `webapp/static` must be created before the `index.html` file can be written.
*   **Broken Script Link**: The `<script src="/static/app.js">` link will be broken when opening the HTML file directly from the local filesystem (`file://...`). This is expected behaviour, as the path is absolute from the server root and requires a web server to function correctly. The task is only to create the static asset, not serve it.
*   **Test Fragility**: The recommended string-based test is simple but can be brittle. Minor formatting changes in the HTML (e.g., `id = "todo-input"`) could cause it to fail. This is an acceptable trade-off to avoid adding a new dependency like `BeautifulSoup` for a simple check.

## Sources
*   MDN Web Docs - A guide to Flexbox: [https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox)
*   MDN Web Docs - `script` Element (`defer` attribute): [https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-defer](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-defer)
*   CSS-Tricks - A Complete Guide to Flexbox: [https://css-tricks.com/snippets/css/a-guide-to-flexbox/](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
*   pytest Documentation - [https://docs.pytest.org/](https://docs.pytest.org/)
