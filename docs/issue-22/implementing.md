# IMPLEMENTING - Issue #22

### FILE: webapp/static/index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ToDo List</title>
    <style>
        /* Basic Reset */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* Body Styles */
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background-color: #f5f5f5;
            color: #333;
            padding-top: 40px;
        }

        /* Main Container */
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 24px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* Header */
        h1 {
            text-align: center;
            margin-bottom: 24px;
            color: #222;
        }

        /* Form Section */
        form {
            display: flex;
            gap: 8px;
            margin-bottom: 24px;
        }

        #todo-input {
            flex-grow: 1;
            padding: 10px 14px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }

        #todo-input:focus {
            outline: none;
            border-color: #007bff;
        }

        #add-btn {
            padding: 10px 20px;
            border: none;
            background-color: #007bff;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        #add-btn:hover {
            background-color: #0056b3;
        }

        /* Task List Section */
        #todo-list {
            list-style: none;
        }

        #todo-list li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
            transition: background-color 0.2s;
        }
        
        #todo-list li:last-child {
            border-bottom: none;
        }

        #todo-list li:hover {
            background-color: #f9f9f9;
        }

        .delete-btn {
            background-color: transparent;
            border: none;
            color: #dc3545;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 4px;
        }
        
        .delete-btn:hover {
            color: white;
            background-color: #c82333;
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

        <section id="task-list-section">
            <ul id="todo-list">
                <!-- Tasks will be dynamically inserted here by JavaScript -->
            </ul>
        </section>
    </div>

    <script src="/static/app.js"></script>
</body>
</html>
```

### FILE: tests/test_html.py
```python
import pathlib

def test_index_html_content():
    """
    Tests that the main index.html file contains the required elements.
    """
    # Construct a path to the HTML file relative to this test file's location
    # tests/test_html.py -> ../webapp/static/index.html
    project_root = pathlib.Path(__file__).parent.parent
    html_file_path = project_root / "webapp" / "static" / "index.html"

    assert html_file_path.exists(), f"File not found at {html_file_path}"

    content = html_file_path.read_text(encoding="utf-8")

    # Check for the presence of key element IDs and script references
    assert 'id="todo-input"' in content, "The todo input field is missing its ID."
    assert 'id="add-btn"' in content, "The add button is missing its ID."
    assert 'id="todo-list"' in content, "The todo list container is missing its ID."
    assert 'src="/static/app.js"' in content, "The reference to app.js is missing or incorrect."
    assert '<title>ToDo List</title>' in content, "The page title is incorrect."
```

## Decisions Made
1.  **Form Element**: The issue described a "form section" but didn't explicitly ask for a `<form>` tag. I decided to wrap the input and button in a `<form>` tag as it is semantically correct and standard practice. I also gave it an ID (`todo-form`) for potential future use and added `type="submit"` to the button. This prevents default browser form submission behavior from reloading the page, which is crucial for a single-page app, but the JavaScript part (not in this issue) will handle the `event.preventDefault()`.
2.  **CSS Class for Delete Button**: Although the JavaScript will create the list items, the CSS needs a way to target the delete button. I defined a `.delete-btn` class with the required styling (red 'X' look) and hover effect. The future JavaScript code will be responsible for adding this class to the dynamically created delete buttons.
3.  **Path Resolution in Test**: As planned in the RESEARCHING phase, I used `pathlib` to create a robust path to the `index.html` file from the test file's location. This ensures the test is not dependent on the current working directory from which `pytest` is run.

## Notes
- The directories `webapp/` and `webapp/static/` are created by writing the `webapp/static/index.html` file.
- The `app.js` file is referenced in the HTML but has not been created as per the issue's instructions. This is expected and will be handled in a future task.
- The test file `tests/test_html.py` verifies the presence of critical `id` attributes and the `script` tag as requested. I also added a check for the page title for completeness.
- The CSS is fully embedded in the HTML file, and no external libraries are used, following the requirements.
- The design follows modern practices with Flexbox for layout, a clean "card" UI, and subtle user feedback via hover effects.
