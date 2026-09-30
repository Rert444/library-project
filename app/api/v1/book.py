from fastapi import APIRouter, HTTPException, status
from app.schemas.book import BookCreate, BookRead

router = APIRouter(prefix="/books", tags=["Books"])

# Временное хранилище в памяти (согласно заданию Лабы №1)
_books_db: list[BookRead] = []
_next_id: int = 1


@router.get("/", response_model=list[BookRead])
def get_all_books():
    """Получить список всех книг"""
    return _books_db


@router.get("/{book_id}", response_model=BookRead)
def get_book_by_id(book_id: int):
    """Получить книгу по ID"""
    for book in _books_db:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Книга не найдена"
    )


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate):
    """Создать новую книгу"""
    global _next_id

    new_book = BookRead(id=_next_id, **book_data.model_dump())
    _books_db.append(new_book)
    _next_id += 1

    return new_book


@router.put("/{book_id}", response_model=BookRead)
def update_book(book_id: int, book_data: BookCreate):
    """Обновить данные книги"""
    for index, book in enumerate(_books_db):
        if book.id == book_id:
            updated_book = BookRead(id=book_id, **book_data.model_dump())
            _books_db[index] = updated_book
            return updated_book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Книга не найдена"
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    """Удалить книгу"""
    for index, book in enumerate(_books_db):
        if book.id == book_id:
            _books_db.pop(index)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Книга не найдена"
    )