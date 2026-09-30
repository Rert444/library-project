from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    """Схема для создания новой книги"""
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None


class BookRead(BaseModel):
    """Схема ответа (включает ID, который генерирует сервер)"""
    id: int
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None

    class Config:
        from_attributes = True