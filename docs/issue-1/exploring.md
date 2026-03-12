# EXPLORING - Issue #1

## Issue Summary
The user wants to create the data layer for a ToDo application. This involves defining a Pydantic data model for a "Todo" item, implementing an in-memory storage system for these items, and writing tests to verify the storage functionality.

## Relevant Files
The following files will need to be created as they do not currently exist:
- `webapp/__init__.py`: An empty file to mark the `webapp` directory as a Python package.
- `webapp/models.py`: Will contain the Pydantic `Todo` data model.
- `webapp/storage.py`: Will house the in-memory list, ID counter, and functions to add, list, and delete todos.
- `tests/test_storage.py`: Will contain the unit tests for the functions in `webapp/storage.py`.

The following existing files are relevant for context and patterns:
- `requirements.txt`: To check for existing dependencies (like `pydantic`) and to add it if it's missing.
- `tests/`: This directory establishes the project's testing conventions using `pytest`. Existing files like `tests/test_agent.py` and `tests/test_orchestrator.py` show patterns for writing tests, including the use of `pytest` and mocking.
- `src/`: This directory shows the existing coding style, including the use of type hints and function/module organization.

## Existing Patterns
- **Directory Structure:** The project separates application logic (`src/`) from tests (`tests/`). This task introduces a new application component in a new top-level directory, `webapp/`.
- **Testing:** The `tests/` directory is well-established, with a `test_*.py` file for each corresponding module in `src/`. This pattern should be followed by creating `tests/test_storage.py` for `webapp/storage.py`. Tests appear to use `pytest` and mocking via `@patch` from `unittest.mock`, as seen in `tests/test_orchestrator.py`.
- **Typing:** Type hints are used consistently throughout the codebase (e.g., `filepath: str -> list[dict]`). The issue requires continuing this pattern.
- **Naming Conventions:** Functions and variables use `snake_case` (e.g., `list_agent_issues`). The request to name the internal counter `_next_id` follows the convention of using a single leading underscore for internal implementation details.
- **Data Structures:** Functions frequently return dictionaries or lists of dictionaries (e.g., `list_agent_issues() -> list[dict]`), which aligns with the requirements for the `storage.py` functions.

## Dependencies
- **pydantic**: This is a new dependency required for creating the `Todo` model. It will need to be added to `requirements.txt`.
- **datetime**: The standard library `datetime` module will be required to generate ISO format timestamps for `created_at`.
- **pytest**: The testing framework used by the project, as evidenced by the `tests/` directory.

## Observations
- The task introduces a new, self-contained `webapp` component that is functionally separate from the existing AI agent orchestration logic in the `src/` directory.
- The requested in-memory storage is inherently volatile, meaning all data will be lost when the application restarts. This is by design according to the issue description.
- The requirements for testing are specific, covering not just the happy path but also edge cases like deleting a non-existent item and ensuring ID auto-increment logic is correct after a deletion.
