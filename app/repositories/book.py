from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> list[Book]:
        result = await self.session.execute(select(Book).order_by(Book.id))
        return list(result.scalars().all())

    async def get(self, book_id: int) -> Book | None:
        return await self.session.get(Book, book_id)

    async def create(self, data: BookCreate) -> Book:
        book = Book(
            **data.model_dump(),
            copies_available=data.copies_total,
        )
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def update(self, book: Book, data: BookUpdate) -> Book:
        payload = data.model_dump(exclude_unset=True)

        if "copies_total" in payload:
            issued = book.copies_total - book.copies_available
            new_total = payload["copies_total"]
            if new_total < issued:
                raise ValueError(
                    "Нельзя установить общее количество меньше выданных экземпляров"
                )
            book.copies_available = new_total - issued

        for field, value in payload.items():
            setattr(book, field, value)

        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete(self, book: Book) -> None:
        await self.session.delete(book)
        await self.session.commit()