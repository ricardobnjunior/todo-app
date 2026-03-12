"""
This module contains the API routes for the ToDo application.
The main FastAPI application instance is created here.
"""
from fastapi import FastAPI

# The main FastAPI app instance for the API.
# The server.py file will import this and add frontend serving capabilities.
app = FastAPI()

# Placeholder in-memory "database".
# In a real application, this would be replaced by a proper database connection.
# For the purpose of these issues, it will be expanded to a more stateful manager.
todos_db = []


@app.get("/api/todos")
async def get_todos():
    """
    Returns the list of all ToDo items.
    """
    return todos_db
