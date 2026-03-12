# RESEARCHING - Issue #3

## Research Findings
Creating a static HTML page with embedded CSS is a fundamental web development task. The best practices involve:

1.  **HTML5 Structure:** Use a standard HTML5 boilerplate (`<!DOCTYPE html>`). Employ semantic elements like `<main>`, `<header>`, and `<section>` to improve accessibility and document structure. The `<form>` element is appropriate for the input field and button. The `<script>` tag should be placed just before the closing `</body>` tag to prevent render-blocking, ensuring the page content is visible as quickly as possible.

2.  **CSS Layout with Flexbox:** For the required layout (centered container, side-by-side elements, space-between elements), CSS Flexbox is the modern and most suitable approach.
    *   `display: flex` on the `<body>` can center the main container.
    *   A wrapper `div` around the input and button with `display: flex` can align them horizontally. `flex-grow: 1` on the input will make it take up the available space.
    *   `display: flex` with `justify-content: space-between` on the list items (`<li>`) will position the task title on the left and the delete button on the right.

3.  **Embedded CSS:** Placing CSS within a `<style>` tag in the `<head>` is a straightforward method for single-page applications or simple static pages. It avoids the need for an extra HTTP request for an external stylesheet. Selectors should be as specific as needed. The issue requires using ID selectors (`#todo-input`, `#add-btn`, `#todo-list`), which are appropriate for unique landmark elements.

4.  **Python Testing:** For testing the existence of elements in a static HTML file, a simple approach is sufficient. The test can open the file, read its contents into a string, and use `assert 'substring' in content` to verify that the required `id` attributes and script names are present. This method is simple, has no external dependencies beyond a test runner like `pytest`, and directly fulfills the issue's requirements. Using a full HTML parser like BeautifulSoup would be overly complex for this validation task.

## Duplication Check
The repository contains a completely separate backend logic written in Python for an AI agent system (`src/`, `tests/`) and a data dashboard (`dashboard/`). There is an `index.html` file in the root directory, which appears to be for project documentation.

There is **no existing HTML or CSS code** that is intended for a web application frontend like the one required by this issue. The styles, structure, and purpose are entirely new. Therefore, the `webapp/static/index.html` and `tests/test_html.py` files must be created from scratch. The directory structure `webapp/static/` will also be new.

## Recommended Approach
1.  **Create Directories:** First, create the `webapp` and `webapp/static` directories.

2.  **Create `webapp/static/index.html`:**
    *   Start with a standard HTML5 boilerplate.
    *   Set the page title to "ToDo List".
    *   Create a `<style>` block in the `<head>`.
    *   Inside the `<style>` block, implement the required styling using Flexbox for layouts. Use `body` styles for the background and centering, container styles for the white card effect, and flex rules for the form and list items as researched. Use the specified fonts and colors.
    *   In the `<body>`, create the HTML structure with a main container `div`, an `<h1>` header, a `form`, and a `<ul>` with the specified IDs (`todo-input`, `add-btn`, `todo-list`).
    *   Place `<script src="/static/app.js"></script>` at the end of the `<body>`.

3.  **Create `tests/test_html.py`:**
    *   Create a new test file `tests/test_html.py`.
    *   Add a test function, e.g., `test_index_html_content`.
    *   In this function, open and read the contents of `webapp/static/index.html`.
    *   Assert that the file content contains the required substrings: `"todo-input"`, `"add-btn"`, `"todo-list"`, and `"app.js"`. This validates the key requirements of the issue simply and effectively.

This approach directly implements the requirements using standard, modern web practices without introducing unnecessary complexity or dependencies.

## Risks and Edge Cases
*   **File Path Error:** The new file must be created at `webapp/static/index.html`. Creating it in the root would overwrite a different, existing `index.html`. The new directories `webapp/` and `webapp/static/` must be created first.
*   **Broken Script Link:** The HTML will reference `app.js`, which does not exist yet. This will result in a 404 error in the browser's developer console when viewing the page. This is an expected outcome as per the issue description, which defers JavaScript creation to a later task.
*   **CSS Style Specificity:** Since all CSS is embedded and selectors are based on unique IDs as requested, conflicts are unlikely. This is a simple page.
*   **Test Brittleness:** The tests rely on substring matching. While sufficient for this task, they could pass even if the HTML is malformed but contains the required strings. This is an acceptable trade-off for simplicity, as the primary goal is to check for the existence of the specified IDs and script reference.

## Sources
*   MDN Web Docs - A basic HTML document: [https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started#anatomy_of_an_html_document](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started#anatomy_of_an_html_document)
*   MDN Web Docs - A Complete Guide to Flexbox: [https://css-tricks.com/snippets/css/a-guide-to-flexbox/](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
*   MDN Web Docs - script: The Script element: [https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#usage_notes](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#usage_notes)
*   pytest Documentation - Asserting with the assert statement: [https://docs.pytest.org/en/stable/how-to/assert.html](https://docs.pytest.org/en/stable/how-to/assert.html)
