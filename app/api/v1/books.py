from fastapi import APIRouter, HTTPException, status

from app.api.deps import BookRepoDep
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookRead])
async def list_books(repo: BookRepoDep) -> list[BookRead]:
    return await repo.list()


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, repo: BookRepoDep) -> BookRead:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(data: BookCreate, repo: BookRepoDep) -> BookRead:
    return await repo.create(data)


@router.put("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int, data: BookUpdate, repo: BookRepoDep
) -> BookRead:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    try:
        return await repo.update(book, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, repo: BookRepoDep) -> None:
    book = await repo.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    await repo.delete(book)