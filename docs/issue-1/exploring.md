# EXPLORING - Issue #1

## Issue Summary
The task is to create the data layer for a ToDo list application. This involves creating a Pydantic data model for a "todo" item, implementing in-memory storage functions for creating, listing, and deleting todos, and writing corresponding tests.

## Relevant Files
The issue requires the creation of several new files. The structure of the existing `tests` directory is also relevant for establishing testing patterns.

*   `webapp/__init__.py`: (To be created) An empty file to mark the `webapp` directory as a Python package.
*   `webapp/models.py`: (To be created) This file will contain the Pydantic `Todo` data model.
*   `webapp/storage.py`: (To be created) This file will house the in-memory list for storing todos and the functions to interact with it (`add_todo`, `list_todos`, `delete_todo`).
*   `tests/test_storage.py`: (To be created) This file will contain unit tests for the functions in `webapp/storage.py`.
*   `requirements.txt`: Relevant because the `pydantic` library, a new dependency, will need to be added here.
*   `tests/*.py`: Existing test files (e.g., `test_agent.py`, `test_orchestrator.py`) are relevant as they establish the patterns and conventions for writing tests in this repository.

## Existing Patterns
*   **Project Structure**: The repository is organized with distinct top-level directories for different concerns: `src` for core application logic, `tests` for testing, and `dashboard` for a UI component. The issue introduces a new `webapp` directory, which seems to follow this pattern of creating a new, separate component.
*   **Module and File Naming**: Files use `snake_case` (e.g., `github_client.py`, `repo_context.py`).
*   **Test File Naming**: Test files are prefixed with `test_` (e.g., `test_agent.py`, `test_duplication_checker.py`), which is standard for `pytest` discovery.
*   **Typing**: Python type hints are used throughout the codebase in function signatures (e.g., `extract_function_signatures(filepath: str) -> list[dict]`). The issue requires continuing this pattern.
*   **Data Transfer Objects**: Simple dictionaries (`dict`) and lists of dictionaries (`list[dict]`) are frequently used as return types for functions that fetch or process data (e.g., `list_agent_issues`, `fetch_pull_requests`). The issue's requirements for the storage functions to return `dict` and `list[dict]` align with this pattern.
*   **Testing Conventions**:
    *   The `tests` directory mirrors the `src` directory structure.
    *   `unittest.mock.patch` is used for mocking dependencies, as seen in `tests/test_orchestrator.py`.
    *   Helper functions, often prefixed with an underscore (`_`), are used to create test data and set up test environments (e.g., `_create_project` in `test_duplication_checker.py`, `_make_pr` in `test_dashboard.py`).
*   **Internal Function Naming**: Internal or private helper functions within modules are sometimes prefixed with an underscore, a convention the issue follows by naming the ID counter `_next_id`.

## Dependencies
*   **Pydantic**: This is a new external dependency required for creating the `Todo` model in `webapp/models.py`. It will need to be added to `requirements.txt`.
*   **datetime**: The standard library `datetime` module will be implicitly needed in `webapp/storage.py` to generate the `created_at` timestamp in ISO format.
*   **pytest**: The testing framework used in the project, which will be necessary to run the new tests in `tests/test_storage.py`.

## Observations
*   **New Application Component**: The issue describes adding a "ToDo list application" (`webapp`), which is functionally unrelated to the existing codebase's focus on an AI agent orchestrator interacting with GitHub. This new `webapp` appears to be a self-contained module.
*   **In-Memory State**: The `storage.py` module is specified to use module-level variables (`todos: list`, `_next_id: int`) for data storage. This means the application state is transient and will be reset every time the application restarts.
*   **Model vs. Storage Representation**: The issue requires creating a Pydantic `Todo` model but specifies that the in-memory storage list (`todos`) should be a `list[dict]` and that the `add_todo` and `list_todos` functions should return `dict` and `list[dict]`, respectively. This implies the Pydantic model may be intended for data definition and validation, while the runtime storage and function interfaces will use plain dictionaries.
