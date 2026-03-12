# EXPLORING - Issue #1

## Issue Summary
The user wants to create a data layer for a ToDo application. This involves creating a new `webapp` directory with a Pydantic data model for a `Todo` item, an in-memory storage module to manage a list of todos, and corresponding tests for the storage functions.

## Relevant Files
Since this task involves creating new functionality, most relevant files do not yet exist.
- `webapp/__init__.py` (to be created): Required to make `webapp` a Python package.
- `webapp/models.py` (to be created): Will contain the `Todo` Pydantic data model.
- `webapp/storage.py` (to be created): Will house the in-memory list of todos and functions to manipulate it (`add_todo`, `list_todos`, `delete_todo`).
- `tests/test_storage.py` (to be created): Will contain unit tests for the functions in `webapp/storage.py`.
- `requirements.txt`: May need to be updated to include `pydantic` if it is not already a dependency.

## Existing Patterns
- **Project Layout:** The project separates application logic (`src/`) from tests (`tests/`). This task introduces a new top-level directory, `webapp`, which differs from the existing `src` layout.
- **Testing:**
    - Tests are located in the `tests/` directory.
    - Test files are named using the `test_*.py` convention.
    - Test functions are named using the `test_*()` convention.
    - `unittest.mock.patch` is used for mocking dependencies, as seen in `tests/test_orchestrator.py`.
    - Helper functions in test files are often prefixed with an underscore (e.g., `_create_temp_project` in `tests/test_repo_context.py`).
- **Coding Style:**
    - Python code uses type hints extensively (e.g., `filepath: str`, `list[dict]`).
    - Function and variable names follow the `snake_case` convention.
- **Data Handling:** The use of `list[dict]` is a common pattern for handling collections of objects, as seen in `src/github_client.py`'s `list_agent_issues` function.

## Dependencies
- **Pydantic:** The issue explicitly requires using a Pydantic model. This will likely be a new external dependency for the project.
- **datetime (standard library):** Required for generating the `created_at` timestamp.
- **Pytest:** The existing test suite appears to use Pytest, and the new tests should follow this convention.

## Observations
- The task introduces a new "webapp" domain into a repository that is otherwise focused on being a GitHub agent orchestrator. This new functionality seems distinct from the existing `src` codebase.
- The issue specifies that the `Todo` model should be Pydantic, but the `storage` module should work with and return plain dictionaries (`list[dict]`), not Pydantic model instances. This implies a separation between the data structure definition and its in-memory representation.
- The project structure does not yet contain a `webapp` directory, so it will need to be created at the root level as requested.
