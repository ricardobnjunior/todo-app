from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Todo(BaseModel):
    """
    Pydantic model for a ToDo item.
    """
    id: int
    title: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
