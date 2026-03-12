from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Todo(BaseModel):
    """
    Pydantic model representing a single ToDo task.
    """
    id: int
    title: str
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
