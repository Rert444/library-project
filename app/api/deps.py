from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.book import BookRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_book_repository(session: SessionDep) -> BookRepository:
    return BookRepository(session)


BookRepoDep = Annotated[BookRepository, Depends(get_book_repository)]