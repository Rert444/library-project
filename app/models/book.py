# app/models/book.py
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text, func, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # УДАЛЯЕМ СТАРОЕ ПОЛЕ author, ВМЕСТО НЕГО:
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    genre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    copies_total: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    copies_available: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Связь: книга принадлежит одному автору
    author: Mapped["Author"] = relationship(back_populates="books")