# EXPLORING - Issue #20

## Issue Summary
The task is to create the data layer for a ToDo list application. This involves defining a Pydantic data model for a "todo" item, implementing an in-memory storage system to manage these items, and writing tests to verify the storage logic.

## Relevant Files
This task requires the creation of new files, as the `webapp` module does not exist yet.
- `webapp/__init__.py`: To be created as an empty file to define `webapp` as a Python package.
- `webapp/models.py`: To be created to house the `Todo` Pydantic model.
- `webapp/storage.py`: To be created to implement the in-memory CRUD operations (`add`, `list`, `delete`) for todos.
- `tests/test_storage.py`: To be created in the existing `tests` directory to unit test the functionality of `webapp/storage.py`.
- `requirements.txt`: This file is relevant as the `pydantic` library, a new dependency required for `webapp/models.py`, will need to be added to it.

## Existing Patterns
- **Directory Structure**: The project separates application logic into a top-level `src` directory and tests into a `tests` directory. The new `webapp` directory will be a new top-level directory, parallel to `src`.
- **Naming Conventions**:
    - Function and variable names use `snake_case` (e.g., `list_agent_issues`, `chat_with_history`). The issue follows this with `add_todo`, `list_todos`.
    - Internal or private module-level variables are prefixed with an underscore (e.g., `_get_client`). The issue follows this by naming the id counter `_next_id`.
- **Typing**: The existing codebase uses Python's type hints extensively (e.g., `filepath: str -> list[dict]`, `messages: list[dict]`). The issue description also specifies types for the new functions.
- **Testing**: Tests are located in the `tests/` directory. Pytest appears to be the framework of choice, as evidenced by the `test_*.py` file naming convention. Mocks are used for testing functions with external dependencies or side effects, using `@patch` from `unittest.mock` (e.g., `tests/test_orchestrator.py`).
- **Data Exchange**: Using `list[dict]` is a common pattern for returning collections of objects from functions, as seen in `src/github_client.py:list_agent_issues`. The issue requires the storage functions to return `dict` and `list[dict]`.

## Dependencies
- **pydantic**: This is a new external dependency required to create the `Todo` data model in `webapp/models.py`.
- **datetime**: A standard library module that will be required in `webapp/storage.py` to generate the `created_at` timestamp.

## Observations
- The new `webapp` will exist as a separate top-level package alongside `src`, suggesting a monorepo structure with multiple, potentially independent applications.
- Although `webapp/models.py` will define a Pydantic `Todo` model, the functions in `webapp/storage.py` are specified to return `dict` and `list[dict]`. This implies that the Pydantic model will likely be used for data validation and structure, with its instances converted to dictionaries before being returned from the storage layer.
- The ID generation logic requires the counter to increment even after items are deleted (e.g., creating 1, 2, 3, deleting 2, and then creating a new item with ID 4), which is a standard auto-increment pattern.
- The existing project is an AI agent orchestrator. The ToDo list application appears to be a separate, new piece of functionality being added to the same repository.
