import os
import pathlib

def test_usage_documentation_exists_and_has_key_sections():
    """
    Checks if the USAGE.md file exists, is not empty, and contains key sections.
    """
    # Use pathlib for a more modern, object-oriented approach to paths.
    # The path is relative to the project root where tests are typically run.
    doc_path = pathlib.Path("webapp/docs/USAGE.md")

    # 1. Verify the file exists
    assert doc_path.exists(), f"Documentation file not found at: {doc_path}"

    # 2. Read the file using UTF-8 and verify it's not empty
    content = doc_path.read_text(encoding="utf-8")
    
    assert content, "Documentation file is empty."

    # 3. Verify key sections are present
    key_sections = [
        "Como rodar",
        "Como usar",
        "API endpoints"
    ]

    for section in key_sections:
        assert f"## {section}" in content or f"# {section}" in content, \
               f"Key section header '## {section}' not found in documentation."
