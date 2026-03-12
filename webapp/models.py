from datetime import datetime, timezone
from pydantic import BaseModel, Field

def _generate_utc_iso_string() -> str:
    """
    Generates the current time in UTC as an ISO 8601 formatted string.
    """
    return datetime.now(timezone.utc).isoformat()


class Todo(BaseModel):
    """
    Represents a single ToDo task.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=_generate_utc_iso_string)
