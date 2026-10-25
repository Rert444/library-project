from fastapi import APIRouter, status, Query
from app.api.deps import BookRepoDep, CurrentUserDep, BookServiceDep
from app.schemas.book import BookCreate, BookRead, BookUpdate, BookList

router = APIRouter(prefix="/books", tags=["books"])

# ВРЕМЕННЫЙ МАРШРУТ ДЛЯ АВТОРОВ (пока оставляем как есть, так как для него нет сервиса)
@router.post("/authors/", tags=["authors"])
async def create_author_test(
        name: str,
        repo: BookRepoDep,
        current_user: CurrentUserDep
):
    from fastapi import HTTPException
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
        service: BookServiceDep,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=100),
        sort_by: str = Query("id"),
        order: str = Query("asc", pattern="^(asc|desc)$"),
        genre: str | None = Query(None),
        is_archived: bool | None = Query(None),
):
    return await service.get_all(
        page=page, size=size, sort_by=sort_by,
        order=order, genre=genre, is_archived=is_archived
    )


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, service: BookServiceDep) -> BookRead:
    return await service.get_by_id(book_id)


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(
        data: BookCreate,
        service: BookServiceDep,
        current_user: CurrentUserDep
) -> BookRead:
    return await service.create(data, current_user.role)


@router.put("/{book_id}", response_model=BookRead)
async def update_book(
        book_id: int,
        data: BookUpdate,
        service: BookServiceDep,
        current_user: CurrentUserDep
) -> BookRead:
    return await service.update(book_id, data, current_user.role)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        service: BookServiceDep,
        current_user: CurrentUserDep
) -> None:
    await service.delete(book_id, current_user.role)