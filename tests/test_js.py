import os

def test_app_js_content():
    """
    Tests that webapp/static/app.js contains the required function names and keywords.
    """
    js_file_path = 'webapp/static/app.js'
    
    # This check ensures that the file exists before we try to read it.
    # In a CI/CD pipeline, the file should be available from checkout.
    assert os.path.exists(js_file_path), f"JavaScript file not found at {js_file_path}"

    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required keywords and function definitions
    assert "loadTodos" in content, "Function 'loadTodos' not found in app.js"
    assert "addTodo" in content, "Function 'addTodo' not found in app.js"
    assert "deleteTodo" in content, "Function 'deleteTodo' not found in app.js"
    assert "/api/todos" in content, "API endpoint '/api/todos' not found in app.js"
    assert "fetch" in content, "The 'fetch' API call not found in app.js"
    assert "DOMContentLoaded" in content, "Event listener for 'DOMContentLoaded' not found in app.js"
