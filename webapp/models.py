"""
Data models for the ToDo application.
"""
from pydantic import BaseModel, Field
from datetime import datetime, timezone


def _generate_iso_timestamp() -> str:
    """Returns the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class Todo(BaseModel):
    """
    Represents a single ToDo task.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=_generate_iso_timestamp)
