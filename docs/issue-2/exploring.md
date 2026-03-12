# EXPLORING - Issue #2

## Issue Summary
The goal is to create a REST API for a ToDo application using FastAPI. This involves creating endpoints for listing, adding, and deleting todos, implementing CORS, and writing corresponding tests using FastAPI's `TestClient`.

## Relevant Files
- `webapp/api.py` (Does not exist): This file will be created to house the `FastAPI` application, including the API router and the CRUD endpoints (`/api/todos`).
- `webapp/storage.py` (Does not exist): This module is mentioned as the source for data persistence functions (`add_todo`, `delete_todo`). The API implementation will depend on it.
- `tests/test_api.py` (Does not exist): This file will be created to contain the tests for the new API endpoints, verifying status codes and JSON responses for create, read, and delete operations.
- `requirements.txt`: This file lists the project's Python dependencies. It will need to include `fastapi` and an ASGI server like `uvicorn` for the application to run. `pytest` would be needed for testing.
- `index.html`: This file exists at the root. It is likely the frontend that will consume the API, which explains the requirement for CORS middleware.

## Existing Patterns
- **Testing**: The `tests/` directory shows a clear pattern of using `pytest` for testing. Test files are named `test_*.py` and contain test functions named `test_*`. `unittest.mock.patch` is heavily used to mock dependencies and isolate components during tests.
- **Project Structure**: The codebase is organized into distinct directories based on functionality (`src`, `dashboard`, `tests`). The issue proposes creating a new `webapp` directory, which aligns with this modular approach.
- **Web Applications**: There is an existing web application in `dashboard/app.py`. However, it seems to be a data dashboard (potentially using Dash or Flask) and is separate from the new FastAPI service requested.
- **Dependency Management**: A `requirements.txt` file is used to manage Python package dependencies.

## Dependencies
- **External Libraries**: The task explicitly requires using `FastAPI` and its `TestClient`. This implies dependencies on `fastapi`, `uvicorn` (or another ASGI server), and `pytest`.
- **Internal Modules**: The new `webapp/api.py` will have a crucial dependency on a `webapp.storage` module to handle the business logic of managing todos.

## Observations
- The core of the existing repository (`src/`, `tests/`) is an AI agent orchestration system that interacts with GitHub issues and LLMs. The requested ToDo API is a new, self-contained feature that does not seem to interact with the existing agent logic.
- Key files and directories required for this task, namely `webapp/api.py`, `webapp/storage.py`, and `tests/test_api.py`, do not currently exist in the repository. They will need to be created from scratch.
- The requirement for `CORS (allow all origins)` indicates that the API will be called from a different origin, most likely the `index.html` file served as a static page in the browser.
- The current `requirements.txt` does not contain `fastapi` or `uvicorn`, so these will need to be added.
