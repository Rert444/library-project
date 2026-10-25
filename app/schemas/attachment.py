from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttachmentRead(BaseModel):
    id: int
    filename: str
    content_type: str
    size: int
    book_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)