from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, page: int = 1, size: int = 10, sort_by: str = "id", order: str = "asc",
                   genre: str | None = None, is_archived: bool | None = None) -> dict:
        query = select(Book).options(selectinload(Book.author))

        if genre:
            query = query.where(Book.genre == genre)
        if is_archived is not None:
            query = query.where(Book.is_archived == is_archived)

        if order == "desc":
            query = query.order_by(getattr(Book, sort_by).desc())
        else:
            query = query.order_by(getattr(Book, sort_by).asc())

        total_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(total_query)

        query = query.offset((page - 1) * size).limit(size)
        result = await self.session.execute(query)
        items = list(result.scalars().all())

        return {"items": items, "total": total, "page": page, "size": size,
                "pages": (total + size - 1) // size if total > 0 else 0}

    async def get(self, book_id: int) -> Book | None:
        query = select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: BookCreate) -> Book:
        book = Book(
            title=data.title,
            author_id=data.author_id,
            genre=data.genre,
            year=data.year,
            description=data.description,
            copies_total=data.copies_total,
            copies_available=data.copies_total,
            is_archived=data.is_archived,
        )
        self.session.add(book)
        await self.session.commit()
        return await self.get(book.id)

    async def update(self, book: Book, data: BookUpdate) -> Book:
        payload = data.model_dump(exclude_unset=True)
        if "copies_total" in payload:
            issued = book.copies_total - book.copies_available
            new_total = payload["copies_total"]
            if new_total < issued:
                raise ValueError("Нельзя установить общее количество меньше выданных экземпляров")
            book.copies_available = new_total - issued
        for field, value in payload.items():
            setattr(book, field, value)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete(self, book: Book) -> None:
        await self.session.delete(book)
        await self.session.commit()