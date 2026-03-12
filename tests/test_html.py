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
