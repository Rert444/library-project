from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    genre: str | None = Field(default=None, max_length=100)
    year: int | None = Field(default=None, ge=0, le=2100)
    description: str | None = None
    copies_total: int = Field(default=1, ge=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=255)
    genre: str | None = Field(default=None, max_length=100)
    year: int | None = Field(default=None, ge=0, le=2100)
    description: str | None = None
    copies_total: int | None = Field(default=None, ge=0)


class BookRead(BookBase):
    id: int
    copies_available: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)