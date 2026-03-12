# RESEARCHING - Issue #22

## Research Findings
### HTML Best Practices
- **Structure:** A standard HTML5 document structure should be used, starting with `<!DOCTYPE html>`. The `<head>` section should include `meta` tags for character set (`<meta charset="UTF-g">`) and viewport for responsive design (`<meta name="viewport" content="width=device-width, initial-scale=1.0">`), as well as the page `<title>`.
- **Semantics:** Using semantic elements like `<main>`, `<header>`, and `<section>` can improve accessibility and document structure, though the requirements are for basic `div`s which is also acceptable. The core elements are the `<form>`, `<input>`, `<button>`, and `<ul>`.
- **Script Placement:** Placing the `<script>` tag just before the closing `</body>` tag is a standard performance best practice. It ensures the HTML content is parsed and rendered by the browser before it downloads and executes the JavaScript, improving the perceived load time for the user.

### CSS Best Practices
- **Layout:** For arranging the input field and button, and the task text and delete button, CSS Flexbox is the modern and most suitable approach.
    - `display: flex;` on a container will create a flex context.
    - `flex-grow: 1;` on the input field will make it take up all available space.
    - `justify-content: space-between;` on list items will push the task title and the delete button to opposite ends.
    - `align-items: center;` will vertically center items in the flex container.
- **Centering:** The standard method for centering a block-level element with a fixed `max-width` is to set its horizontal margins to auto (`margin: 20px auto;`).
- **Styling:**
    - A basic CSS reset, such as `* { box-sizing: border-box; margin: 0; padding: 0; }`, is useful to ensure consistent rendering across browsers.
    - Using a `system-ui` font stack (`font-family: system-ui, sans-serif;`) is a modern practice that leverages the native operating system's font for better performance and a familiar look.
    - Effects like `box-shadow` for the card and `cursor: pointer` and a `background-color` change for hover effects on buttons and list items improve user experience.
- **Embedded CSS:** Placing CSS within a `<style>` tag in the `<head>` is a valid approach for single-page applications or small projects to avoid an extra network request for an external stylesheet.

### Python Testing
- **File I/O:** The test will need to read the `webapp/static/index.html` file. Using Python's standard library (`pathlib` is recommended) to construct a path relative to the test file's location is a robust way to ensure the test can run from any directory.
- **Assertions:** The requirement is to check for the presence of specific substrings (`"todo-input"`, `"add-btn"`, etc.). A simple `assert "substring" in file_content` is sufficient and directly meets the needs of the issue.

## Duplication Check
- **HTML/Frontend:** The codebase contains `index.html` in the root and `escopo/system-overview.html`. These appear to be for documentation or other purposes and not a web application frontend. The dashboard (`dashboard/app.py`) is a Flask application but does not contain any static HTML templates that could be reused; it seems to be API-driven or server-side rendered without a comparable structure. Therefore, creating `webapp/static/index.html` will be a new addition without duplicating existing application logic or UI.
- **Testing:** The `tests/` directory contains many test files. While none of them test static HTML, they establish a clear pattern of using `pytest` and naming test files `test_*.py`. A new file `tests/test_html.py` will fit this pattern perfectly. There are no existing test helpers for reading project files that can be reused; the test will need simple, self-contained file I/O logic.

## Recommended Approach
1.  **Create Directories:** First, create the `webapp/` directory and the `webapp/static/` subdirectory.
2.  **HTML File (`index.html`):**
    -   Create `webapp/static/index.html`.
    -   Start with HTML5 boilerplate (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`).
    -   In `<head>`, add the title "ToDo List", charset meta tag, and the embedded CSS within a `<style>` tag.
    -   In `<body>`, create the specified structure: a main container `div`, an `<h1>` header, a `<form>` containing the `input#todo-input` and `button#add-btn`, and an empty `<ul id="todo-list">`.
    -   Add the `<script src="/static/app.js"></script>` tag at the end of the `<body>`.
3.  **Embedded CSS:**
    -   Inside the `<style>` tag, define styles for the `body` (background color, font).
    -   Style the main container to be centered with a max-width and have a "card" appearance using `padding`, `background-color`, `border-radius`, and `box-shadow`.
    -   Use `display: flex` on the form to place the input and button side-by-side. The input should have `flex-grow: 1`.
    -   Define styles for future `li` elements inside `#todo-list`, also using `display: flex` and `justify-content: space-between` to position the task text and a delete button. Add a `:hover` effect.
4.  **Test File (`test_html.py`):**
    -   Create `tests/test_html.py`.
    -   Add a test function `test_index_html_contains_elements`.
    -   Inside the test, construct the path to `webapp/static/index.html`. Using `pathlib.Path(__file__).parent.parent / "webapp" / "static" / "index.html"` is a robust way to do this.
    -   Read the file's content.
    -   Use multiple `assert` statements to verify that the strings `id="todo-input"`, `id="add-btn"`, `id="todo-list"`, and `src="/static/app.js"` are present in the content.

This approach directly addresses all requirements using standard, modern web development and Python testing practices, while fitting neatly into the existing project structure.

## Risks and Edge Cases
- **Overwriting Files:** The agent must be careful to create the new `index.html` at `webapp/static/index.html` and not overwrite the existing `index.html` in the project root.
- **Incorrect Paths in Test:** The test must correctly resolve the path to the HTML file from the `tests` directory. A hardcoded relative path (`../webapp/...`) might fail if the test runner's working directory changes. Constructing an absolute path or a path relative to the test file itself is safer.
- **CSS Complexity:** While the requirements are simple, small details matter. Forgetting `align-items: center` might cause vertical misalignment. Not setting `box-sizing: border-box` could lead to layout issues with padding and borders.
- **Future JavaScript Interaction:** The static HTML for the list items should not include placeholder a list item as it will be populated by JavaScript. The `ul` must be empty as requested. The styling for the delete button (e.g., a red 'X') should be defined in the CSS, anticipating its dynamic creation by `app.js`.

## Sources
-   MDN Web Docs - HTML5 element reference
-   MDN Web Docs - A Complete Guide to Flexbox: [https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox)
-   MDN Web Docs - `system-ui` font-family: [https://developer.mozilla.org/en-US/docs/Web/CSS/font-family#system-ui](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family#system-ui)
-   `pytest` documentation: [https://docs.pytest.org/](https://docs.pytest.org/)
-   Python `pathlib` documentation: [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)
