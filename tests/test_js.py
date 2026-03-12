import os

def test_app_js_content():
    """
    Tests that the app.js file contains the required function names and keywords.
    """
    # Define the path to the JavaScript file relative to the project root
    js_file_path = os.path.join('webapp', 'static', 'app.js')

    # Ensure the file exists before trying to open it
    assert os.path.exists(js_file_path), f"JavaScript file not found at: {js_file_path}"

    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for the presence of the required substrings as per the issue requirements
    required_strings = [
        "loadTodos",
        "addTodo",
        "deleteTodo",
        "/api/todos",
        "fetch"
    ]

    for required_string in required_strings:
        assert required_string in content, f"Missing required string '{required_string}' in app.js"
