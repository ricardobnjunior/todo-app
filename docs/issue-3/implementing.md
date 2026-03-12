# IMPLEMENTING - Issue #3

### FILE: webapp/static/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ToDo List</title>
    <style>
        :root {
            --primary-color: #007bff;
            --danger-color: #dc3545;
            --light-gray: #f5f5f5;
            --dark-gray: #333;
            --border-color: #ddd;
        }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--light-gray);
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding-top: 40px;
        }

        .container {
            background-color: #ffffff;
            padding: 2em;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 90%;
            box-sizing: border-box;
        }

        h1 {
            text-align: center;
            color: var(--dark-gray);
            margin-top: 0;
        }

        #todo-form {
            display: flex;
            gap: 10px;
            margin-bottom: 1.5em;
        }

        #todo-input {
            flex-grow: 1;
            padding: 0.75em;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 1rem;
        }

        #add-btn {
            padding: 0.75em 1.5em;
            background-color: var(--primary-color);
            color: #ffffff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
        }

        #add-btn:hover {
            opacity: 0.9;
        }

        #todo-list {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }

        #todo-list li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75em;
            border-bottom: 1px solid var(--border-color);
            transition: background-color 0.2s ease-in-out;
        }

        #todo-list li:first-child {
            border-top: 1px solid var(--border-color);
        }

        #todo-list li:hover {
            background-color: #f9f9f9;
        }

        .task-title {
            flex-grow: 1;
        }

        .delete-btn {
            background-color: var(--danger-color);
            color: #ffffff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 30px;
            height: 30px;
            font-weight: bold;
            font-size: 1rem;
            line-height: 30px;
            text-align: center;
            margin-left: 1em;
        }
        .delete-btn:hover {
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ToDo List</h1>
        <form id="todo-form">
            <input type="text" id="todo-input" placeholder="Digite uma tarefa...">
            <button type="submit" id="add-btn">Adicionar</button>
        </form>
        <ul id="todo-list">
            <!-- Tasks will be added here by JavaScript -->
        </ul>
    </div>

    <script src="/static/app.js"></script>
</body>
</html>
```

### FILE: tests/test_html.py
```python
import os


def test_index_html_content():
    """
    Tests if the index.html file contains the required element IDs and script reference.
    """
    # Construct the path to the HTML file relative to this test file.
    # __file__ -> tests/test_html.py
    # os.path.dirname(__file__) -> tests/
    # os.path.join(..., '..') -> project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, 'webapp', 'static', 'index.html')

    assert os.path.exists(file_path), f"File not found at {file_path}"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for the existence of key element IDs and the script tag
    assert 'id="todo-input"' in content, "Missing todo-input element"
    assert 'id="add-btn"' in content, "Missing add-btn element"
    assert 'id="todo-list"' in content, "Missing todo-list element"
    assert 'src="/static/app.js"' in content, "Missing app.js script reference"

```

## Decisions Made
1.  **Test Assertions:** In `tests/test_html.py`, I decided to check for the full `id="..."` and `src="..."` attributes rather than just the substrings (`"todo-input"`, `"app.js"`). This makes the test slightly more robust by ensuring these strings appear in their intended context as attributes, reducing the chance of a false positive from a comment or plain text.
2.  **CSS for Delete Button:** The issue mentions "a red X button on the right" for list items. While the JavaScript to create this button is out of scope, I pre-emptively added a `.delete-btn` CSS class to the embedded style block. This makes the subsequent JavaScript task easier, as the styles will already be defined.
3.  **Form Element:** I wrapped the input field and button in a `<form>` element (`<form id="todo-form">`). This is semantic HTML and allows for form submission handling (e.g., pressing Enter in the input field), which is standard practice for this kind of UI.
4.  **Test File Path:** I constructed the path to `index.html` within the test dynamically using `os.path.abspath(__file__)`. This ensures the test can be run reliably from any directory, including the project root (which is how `pytest` typically runs).

## Notes
- The directories `webapp/` and `webapp/static/` are implied by the creation of `webapp/static/index.html`. They must be created by the system executing this plan.
- The reference to `/static/app.js` will result in a 404 error if `index.html` is opened in a browser before `app.js` is created. This is expected and aligns with the issue's scope.
- The test file `tests/test_html.py` verifies the presence of required elements but does not validate the full HTML structure or the CSS styles. This is sufficient to meet the issue's testing requirements.
