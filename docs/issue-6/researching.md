# RESEARCHING - Issue #6

## Research Findings
The task is to create a `USAGE.md` documentation file for a ToDo list web application and a corresponding test file.

**Best Practices for User Documentation (Markdown):**
1.  **Structure and Clarity:** The issue provides a good structure for a user guide: a high-level summary, setup instructions, usage instructions, and technical details (API, file structure). Using Markdown headers (`#`, `##`) for sections is standard practice and enhances readability.
2.  **Audience-focused:** The request to keep it "short, clear, and beginner-friendly" is key. This means using simple, non-technical language for the "How to use" section and isolating more technical details (like API endpoints) into their own sections.
3.  **Action-oriented Instructions:** For steps like "How to run" and "How to use", using numbered or bulleted lists with imperative verbs (e.g., "Install dependencies," "Start the server") makes instructions easy to follow.
4.  **Code Formatting:** Commands and code snippets should be enclosed in backticks (`` `code` ``) or code blocks (```) for clarity and to distinguish them from regular text.
5.  **Tables for Structured Data:** For the API endpoints, a Markdown table is the most effective way to present the information clearly, with columns for the HTTP method, path, and description, as requested.
6.  **Language and Encoding:** The document is required in Portuguese (pt-br). Care must be taken to save the file with UTF-8 encoding to correctly handle special characters (e.g., `ç`, `ã`, `é`).

**Best Practices for Testing Documentation:**
1.  **Focus on Existence, Not Content:** It is fragile and generally discouraged to write tests that assert the exact wording of documentation, as it changes frequently. The best practice is to confirm that the documentation exists, is not empty, and contains the main structural elements (like key section headers). This ensures the document is present and has the expected high-level structure without making the test brittle.
2.  **Standard Tooling:** Standard Python libraries (`os` or `pathlib`) are sufficient for these checks. `pytest` is the de-facto standard for testing in Python and is appropriate here.
3.  **Test Location:** Placing the test in `tests/test_docs.py` is consistent with standard Python project layouts, where tests are separated from source code and mirror the structure or topic.

## Duplication Check
The key finding from the `EXPLORING` phase is a **major discrepancy**: the issue describes a ToDo list web application in a `webapp/` directory, while the repository contains an AI agent orchestration framework in a `src/` directory.

-   **No Duplication:** There is no existing code or documentation in the repository for a "ToDo list app." The `webapp/` directory and all its associated files (`server.py`, `static/`, etc.) do not exist. Therefore, creating the `USAGE.md` and `test_docs.py` files will be a net-new addition.
-   **No Refactoring Opportunity:** As there is no similar functionality, there is nothing to extend or refactor. The task must be implemented from scratch based on the issue's requirements.
-   **Existing Patterns:** The project uses `pytest` for testing, and new tests should follow this convention. New documentation files should be in Markdown (`.md`), which is consistent with other documentation in the repository (`README.md`, etc.).

## Recommended Approach
Given the discrepancy, the most logical approach is to follow the issue's requirements literally, which means creating the file structure for the non-existent web application.

1.  **Create Directory Structure:** Create the `webapp/` and `webapp/docs/` directories, as they are required to house the new documentation file.
2.  **Create Documentation File:**
    -   Create `webapp/docs/USAGE.md`.
    -   Write the content in Portuguese (pt-br) following all sections specified in the issue.
    -   Use Markdown for formatting: `##` for headers, backticks for code, and a table for API endpoints.
    -   For the "Estrutura de arquivos" section, invent a plausible and simple file structure for a FastAPI web app, as the actual files do not exist. A sensible structure would be:
        -   `webapp/server.py`: Main FastAPI server file.
        -   `webapp/static/index.html`: Main HTML file for the UI.
        -   `webapp/static/script.js`: JavaScript for frontend logic.
        -   `webapp/docs/USAGE.md`: The documentation file itself.
3.  **Create Test File:**
    -   Create `tests/test_docs.py`.
    -   Write a single test function `test_usage_documentation()`.
    -   Inside the test, use Python's `pathlib.Path` to represent the path to `webapp/docs/USAGE.md`.
    -   Assert that the file exists (`path.exists()`).
    -   Read the file's content using UTF-8 encoding (`path.read_text(encoding="utf-8")`).
    -   Assert that the content is not empty (`assert content`).
    -   Assert that the key required sections are present as substrings in the content (e.g., `assert "Como rodar" in content`).

This approach directly fulfills all stated requirements while being isolated from the existing `src/` codebase.

## Risks and Edge Cases
-   **Repository Inconsistency:** The biggest risk is adding files (`webapp/*`) that are completely unrelated to the rest of the repository's codebase (`src/*`). This is a direct consequence of the mismatch between the issue and the repository's state. The implementation will create a "ghost" application structure.
-   **File Encoding:** The documentation is in Portuguese and must be saved as UTF-8. The test file must also read it as UTF-8. Failure to do so could lead to `UnicodeDecodeError` or incorrect character rendering.
-   **Path Management:** Tests are typically run from the project's root directory. The test file must use a path relative to the root (e.g., `webapp/docs/USAGE.md`) to locate the documentation file correctly.
-   **Fictional File Structure:** The "Estrutura de arquivos" section will be documenting a file structure that doesn't actually exist. This could be confusing, but it is necessary to meet the issue requirements.

## Sources
-   [The Python `pathlib` documentation](https://docs.python.org/3/library/pathlib.html)
-   [pytest official documentation - "Assertions about expected exceptions"](https://docs.pytest.org/en/stable/how-to/assert.html) (General testing patterns)
-   [GitHub Flavored Markdown Spec - Tables](https://github.github.com/gfm/#tables-extension-)
