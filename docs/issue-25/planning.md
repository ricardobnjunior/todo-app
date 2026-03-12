# PLANNING - Issue #25

## Architecture
The solution involves adding new files to the project without modifying any existing code. A new directory structure, `webapp/docs/`, will be created at the project root to house the user documentation. The documentation file, `USAGE.md`, will be created in this new directory.

A corresponding test file, `tests/test_docs.py`, will be added to the existing `tests` directory. This test will not depend on any application source code but will use standard Python libraries (`os`, file I/O) to verify the existence, non-emptiness, and content structure of the `USAGE.md` file. This ensures the documentation artifact meets the requirements and remains intact.

The core of this task is content creation an artifact validation, isolated from the main application's logic.

## Files to Create
### `webapp/docs/USAGE.md`
A Markdown file written in Portuguese (pt-br) containing user documentation for a hypothetical ToDo list application. It will have the following sections:
- **O que e este sistema**: A brief introductory paragraph.
- **Como rodar**: A numbered list of steps to install dependencies and run the server.
- **Como usar**: An unordered list explaining how to add, list, and delete tasks.
- **API endpoints**: A Markdown table listing the three API endpoints (`GET /api/todos`, `POST /api/todos`, `DELETE /api/todos/{id}`).
- **Estrutura de arquivos**: A list describing the purpose of each file in the hypothetical `webapp/` directory.

### `tests/test_docs.py`
A Python test file to validate the `USAGE.md` documentation. It will contain:
- A test function to verify that `webapp/docs/USAGE.md` exists and is not an empty file.
- A test function to read the content of `webapp/docs/USAGE.md` (using UTF-8 encoding) and assert that it contains the key section headers: "Como rodar", "Como usar", and "API endpoints".

## Files to Modify
There are no files to modify. This task only involves the creation of new files and directories.

## TODO List
1. Create the directory `webapp/docs/`. - [simple]
2. Create the file `webapp/docs/USAGE.md` and populate it with all the required sections and content as specified in the issue description, written in Portuguese (pt-br). - [medium]
3. Create the test file `tests/test_docs.py`. - [simple]
4. In `tests/test_docs.py`, implement a test function that verifies `webapp/docs/USAGE.md` exists and is not empty. - [simple]
5. In `tests/test_docs.py`, implement a test function that reads `webapp/docs/USAGE.md` using UTF-8 encoding and asserts that the key section headers ("Como rodar", "Como usar", "API endpoints") are present in the content. - [simple]

## Test Plan
The testing strategy focuses on validating the documentation file itself.
1.  **Existence and Size Test**:
    -   Create a test case in `tests/test_docs.py`.
    -   It will use `os.path.exists()` to confirm `webapp/docs/USAGE.md` is present.
    -   It will use `os.path.getsize()` to ensure the file size is greater than 0.
    -   This test verifies that the documentation file was created correctly and isn't empty.
2.  **Content Structure Test**:
    -   Create a second test case in `tests/test_docs.py`.
    -   This test will open `webapp/docs/USAGE.md` with `encoding="utf-8"`.
    -   It will read the entire file content into a string.
    -   It will then use `assert '...' in content` checks for the presence of the strings "Como rodar", "Como usar", and "API endpoints".
    -   This test ensures that the key required sections are included in the documentation.
