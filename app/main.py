from contextlib import asynccontextmanager
from fastapi import FastAPI

# Импортируем все роутеры
from app.api.v1.book import router as books_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.attachments import router as attachments_router  # НОВОЕ

from app.core.config import settings
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте ничего не делаем, Alembic уже создал таблицы
    yield
    # Корректно закрываем соединения при выключении
    await engine.dispose()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

# Подключаем все роутеры с общим префиксом /api/v1
app.include_router(books_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(attachments_router, prefix="/api/v1")  # НОВОЕ

@app.get("/")
def root():
    return {"message": "Welcome to Library API"}