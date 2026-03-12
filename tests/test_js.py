import os


def test_app_js_content():
    """
    Tests that webapp/static/app.js contains the required keywords.
    This is a simple static check to verify the implementation against requirements.
    """
    # Construct a path relative to this test file to be robust
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    js_file_path = os.path.join(project_root, 'webapp', 'static', 'app.js')

    assert os.path.exists(js_file_path), f"File not found: {js_file_path}"

    with open(js_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    required_keywords = [
        "loadTodos",
        "addTodo",
        "deleteTodo",
        "/api/todos",
        "fetch",
    ]

    for keyword in required_keywords:
        assert keyword in content, f"Keyword '{keyword}' not found in webapp/static/app.js"
