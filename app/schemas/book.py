from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.author import AuthorRead


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author_id: int = Field(..., gt=0)
    genre: str | None = Field(default=None, max_length=100)
    year: int | None = Field(default=None, ge=0, le=2100)
    description: str | None = None
    copies_total: int = Field(default=1, ge=0)
    is_archived: bool = Field(default=False)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author_id: int | None = Field(default=None, gt=0)
    genre: str | None = Field(default=None, max_length=100)
    year: int | None = Field(default=None, ge=0, le=2100)
    description: str | None = None
    copies_total: int | None = Field(default=None, ge=0)
    is_archived: bool | None = None


class BookRead(BookBase):
    id: int
    copies_available: int
    created_at: datetime
    updated_at: datetime
    author: AuthorRead

    model_config = ConfigDict(from_attributes=True)


class BookList(BaseModel):
    items: list[BookRead]
    total: int
    page: int
    size: int
    pages: int