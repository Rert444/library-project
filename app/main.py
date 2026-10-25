from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.book import router as books_router
from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Таблицы теперь создаются через Alembic (alembic upgrade head).
    # При запуске приложения мы просто отдаем управление.
    yield
    # Корректно закрываем соединения с БД при остановке сервера
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

# Подключаем маршруты с префиксом версии API
app.include_router(books_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to Library API"}