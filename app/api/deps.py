from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_session
from app.models.user import User
from app.repositories.book import BookRepository
from app.repositories.user import UserRepository
from app.services.book import BookService  # НОВОЕ

# 1. Зависимость для сессии БД
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# 2. Зависимость для репозитория книг
def get_book_repository(session: SessionDep) -> BookRepository:
    return BookRepository(session)


BookRepoDep = Annotated[BookRepository, Depends(get_book_repository)]


# 3. Зависимость для Сервиса книг (НОВОЕ)
def get_book_service(repo: BookRepoDep) -> BookService:
    return BookService(repo)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]


# 4. Зависимость для получения текущего пользователя (JWT)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: SessionDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repo = UserRepository(session)
    user = await repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


# 5. Аннотированный тип для использования в маршрутах
CurrentUserDep = Annotated[User, Depends(get_current_user)]