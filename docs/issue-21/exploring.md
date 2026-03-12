# EXPLORING - Issue #21

## Issue Summary
The user wants to create a new FastAPI application to provide CRUD (Create, Read, Delete) REST API endpoints for a ToDo list. This includes creating the API endpoints, adding CORS middleware, and writing corresponding tests using FastAPI's TestClient.

## Relevant Files
- `webapp/api.py` (DOES NOT EXIST): This file will need to be created to house the new FastAPI application and its endpoints as specified in the issue.
- `webapp/storage.py` (DOES NOT EXIST): This file is mentioned as a dependency for the API, containing functions like `add_todo` and `delete_todo`. It will need to be created.
- `tests/test_api.py` (DOES NOT EXIST): This test file will need to be created to contain the pytest tests for the new API endpoints.
- `requirements.txt`: This file will need to be updated to include `fastapi` and `uvicorn`, and potentially `httpx` which is used by FastAPI's `TestClient`.
- `tests/`: This directory is relevant as the new test file, `tests/test_api.py`, will be placed here. Existing test files like `test_agent.py` and `test_orchestrator.py` can be used as a reference for testing patterns.
- `index.html`: This file exists at the root of the project. It might be a simple frontend that will consume the API, which would explain the requirement for CORS.

## Existing Patterns
- **Project Structure**: Application code resides primarily in the `src/` directory. The request to create a `webapp/` directory introduces a new top-level module, separate from the existing `src/` and `dashboard/` applications.
- **Testing**: Tests are located in the `tests/` directory with the `test_*.py` naming convention, suggesting `pytest` is the test runner. `unittest.mock.patch` is heavily used across existing tests (`test_agent.py`, `test_orchestrator.py`, `test_llm_client.py`) to mock dependencies and control test environments. Test setup often involves local helper functions (e.g., `_create_temp_project` in `tests/test_repo_context.py`).
- **Coding Conventions**: The codebase consistently uses Python type hints (e.g., `filepath: str -> list[dict]`). The style appears to follow standard Python conventions.

## Dependencies
- **External**: The task will introduce new external dependencies on `fastapi` and `uvicorn`. The testing part will depend on FastAPI's `TestClient`, which requires `httpx`.
- **Internal**: The new `webapp/api.py` module will have an internal dependency on a `webapp.storage` module, which does not currently exist.

## Observations
- The core functionality requested (a ToDo list API) appears entirely unrelated to the existing codebase, which is focused on an AI agent orchestration system that interacts with GitHub.
- The issue requires the creation of a new, self-contained application within the `webapp` directory.
- The `webapp.storage` module is a prerequisite for the API implementation but is not present in the repository and its implementation details (e.g., in-memory vs. file-based) are not specified.
- The requirement for CORS middleware implies that a separate client (like the root `index.html` or a JavaScript-based frontend) will be used to interact with the API.
