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
        /* General Body Styling */
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding-top: 40px;
        }

        /* Main Container */
        .container {
            width: 100%;
            max-width: 600px;
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            box-sizing: border-box;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-top: 0;
            margin-bottom: 20px;
        }

        /* Form for adding new tasks */
        .form-container {
            display: flex;
            margin-bottom: 20px;
        }

        #todo-input {
            flex-grow: 1;
            padding: 12px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 4px 0 0 4px;
            outline: none;
        }

        #todo-input:focus {
            border-color: #007bff;
        }

        #add-btn {
            padding: 0 25px;
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 0 4px 4px 0;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        #add-btn:hover {
            background-color: #0056b3;
        }

        /* Task List */
        #todo-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        /*
         * Styles for dynamically added list items.
         * JavaScript will create <li> elements with a <span> for the text
         * and a <button> for deletion.
         * Example:
         * <li>
         *   <span>Task text here</span>
         *   <button class="delete-btn">X</button>
         * </li>
        */
        #todo-list li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
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
            color: #ff3b30;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            padding: 0 5px;
        }
    </style>
</head>
<body>

    <main class="container">
        <h1>ToDo List</h1>
        <section>
            <!-- Form to add tasks. The outer div helps with layout. -->
            <form onsubmit="return false;" class="form-container">
                <input type="text" id="todo-input" placeholder="Digite uma tarefa...">
                <button id="add-btn">Adicionar</button>
            </form>
        </section>
        <section>
            <!-- The list of tasks will be populated here by JavaScript -->
            <ul id="todo-list">
                <!-- Example of how a list item will look (for styling reference) -->
                <!--
                <li>
                    <span>Example task</span>
                    <button class="delete-btn">X</button>
                </li>
                -->
            </ul>
        </section>
    </main>

    <!-- JavaScript file will be loaded here -->
    <script src="/static/app.js"></script>
</body>
</html>
```

### FILE: tests/test_html.py
```python
import os

def test_index_html_content():
    """
    Tests if key elements required by the JavaScript frontend exist in index.html.
    """
    # Construct the path to the index.html file relative to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_file_path = os.path.join(project_root, 'webapp', 'static', 'index.html')

    assert os.path.exists(html_file_path), "index.html file not found"

    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for the presence of essential IDs and script tag
    assert 'id="todo-input"' in content, "The task input field is missing its ID."
    assert 'id="add-btn"' in content, "The add button is missing its ID."
    assert 'id="todo-list"' in content, "The task list container is missing its ID."
    assert 'src="/static/app.js"' in content, "The app.js script tag is missing or incorrect."

```

## Decisions Made
1.  **CSS Centering**: I chose to use Flexbox on the `<body>` element to center the main container. I used `align-items: flex-start` and `padding-top` instead of `align-items: center` to position the container near the top of the page, which is a more conventional layout for web applications than being perfectly centered vertically.
2.  **Form Submission Prevention**: I added `onsubmit="return false;"` to the `<form>` tag. While the JavaScript is expected to handle form submission gracefully, this prevents an accidental page reload if the JavaScript hasn't loaded or has failed, which is good practice for single-page applications.
3.  **Test Robustness**: For the test file `tests/test_html.py`, I used `os.path.abspath(__file__)` to construct a robust path to `index.html` from the project root. This ensures the test can be run from any directory and still locate the file correctly.
4.  **Test Assertions**: The assertions in the test check for the exact string `id="element-id"` as requested. This is a simple and effective way to meet the requirement without introducing external parsing libraries like BeautifulSoup, thereby keeping the testing dependencies minimal.

## Notes
- The directories `webapp/` and `webapp/static/` must be created in the project root for the files to be placed correctly.
- The `index.html` file links to `/static/app.js`, which does not exist yet. This is expected as per the issue description. Opening the `index.html` file will result in a 404 error in the browser console for `app.js` until it is created in a subsequent task.
- The CSS includes styles for dynamically created list items (`<li>` and `.delete-btn`). I've added comments in the HTML and CSS to clarify that these elements are meant to be generated by JavaScript.
