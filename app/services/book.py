import logging

from fastapi import HTTPException, status

from app.models.book import Book
from app.repositories.book import BookRepository
from app.schemas.book import BookCreate, BookUpdate

logger = logging.getLogger(__name__)


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def get_all(self, **kwargs):
        return await self.repository.list(**kwargs)

    async def get_by_id(self, book_id: int) -> Book:
        book = await self.repository.get(book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book

    async def create(self, data: BookCreate, user_role: str) -> Book:
        if user_role not in ["admin", "manager"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        book = await self.repository.create(data)
        logger.info(f"Создана новая книга: '{data.title}'")
        return book

    async def update(self, book_id: int, data: BookUpdate, user_role: str) -> Book:
        if user_role not in ["admin", "manager"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        book = await self.get_by_id(book_id)
        try:
            updated_book = await self.repository.update(book, data)
            logger.info(f"Обновлена книга ID={book_id}")
            return updated_book
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    async def delete(self, book_id: int, user_role: str) -> None:
        if user_role not in ["admin", "manager"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        book = await self.get_by_id(book_id)
        await self.repository.delete(book)
        logger.info(f"Удалена книга ID={book_id}")