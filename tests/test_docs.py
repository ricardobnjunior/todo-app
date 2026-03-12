import os

DOCS_FILE = 'webapp/docs/USAGE.md'


def test_docs_file_exists_and_is_not_empty():
    """
    Tests if the USAGE.md file exists and is not empty.
    """
    assert os.path.exists(DOCS_FILE), f"Documentation file not found at {DOCS_FILE}"
    assert os.path.getsize(DOCS_FILE) > 0, f"Documentation file {DOCS_FILE} is empty."


def test_docs_file_contains_key_sections():
    """
    Tests if the USAGE.md file contains the required key sections.
    """
    # Ensure the file exists before trying to read it
    assert os.path.exists(DOCS_FILE), f"Documentation file not found at {DOCS_FILE}"

    with open(DOCS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    required_sections = [
        "Como rodar",
        "Como usar",
        "API endpoints"
    ]

    for section in required_sections:
        assert section in content, f"Key section '{section}' not found in {DOCS_FILE}"
