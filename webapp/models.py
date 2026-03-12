"""
Pydantic data models for the webapp.
"""
from datetime import datetime, timezone
from pydantic import BaseModel, Field


def get_current_time_iso() -> str:
    """Returns the current time in UTC ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class Todo(BaseModel):
    """
    Represents a single To-Do item.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=get_current_time_iso)
