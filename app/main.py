from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.api.v1.books import router as books_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app import models  # noqa: F401 — регистрация моделей в Base.metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте приложения.
    # На ЛР №3 это заменим на Alembic-миграции.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закрываем соединения при остановке.
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    lifespan=lifespan,
)

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(books_router)
app.include_router(api_v1)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}