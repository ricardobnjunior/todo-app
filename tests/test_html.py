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
