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
