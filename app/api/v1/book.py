from fastapi import APIRouter, HTTPException, status, Query
from app.api.deps import BookRepoDep, CurrentUserDep  # ДОБАВИЛИ CurrentUserDep
from app.schemas.book import BookCreate, BookRead, BookUpdate, BookList

router = APIRouter(prefix="/books", tags=["books"])


# ВРЕМЕННЫЙ МАРШРУТ ДЛЯ АВТОРОВ (теперь защищен)
@router.post("/authors/", tags=["authors"])
async def create_author_test(
        name: str,
        repo: BookRepoDep,
        current_user: CurrentUserDep  # Защита
):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    from app.models.author import Author
    author = Author(name=name)
    repo.session.add(author)
    await repo.session.commit()
    await repo.session.refresh(author)
    return {"id": author.id, "name": author.name}


@router.get("/", response_model=BookList)
async def list_books(
        repo: BookRepoDep,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        sort_by: str = Query("id"),
        order: str = Query("asc", pattern="^(asc|desc)$"),
        genre: str | None = Query(None),
        is_archived: bool | None = Query(None),
):
    return await repo.list(page=page, size=size, sort_by=sort_by, order=order, genre=genre, is_archived=is_archived)


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, repo: BookRepoDep) -> BookRead:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


# ЗАЩИЩАЕМ СОЗДАНИЕ КНИГИ
@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(
        data: BookCreate,
        repo: BookRepoDep,
        current_user: CurrentUserDep  # Только авторизованные
) -> BookRead:
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await repo.create(data)


# ЗАЩИЩАЕМ ОБНОВЛЕНИЕ КНИГИ
@router.put("/{book_id}", response_model=BookRead)
async def update_book(
        book_id: int,
        data: BookUpdate,
        repo: BookRepoDep,
        current_user: CurrentUserDep  # Только авторизованные
) -> BookRead:
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    try:
        return await repo.update(book, data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


# ЗАЩИЩАЕМ УДАЛЕНИЕ КНИГИ
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        repo: BookRepoDep,
        current_user: CurrentUserDep  # Только авторизованные
) -> None:
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await repo.delete(book)