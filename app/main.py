from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Импортируем все роутеры
from app.api.v1.book import router as books_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.attachments import router as attachments_router

from app.core.config import settings
from app.db.session import engine
from app.core.logging import setup_logging
from app.core.exceptions import http_exception_handler, validation_exception_handler

# Включаем логирование
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    debug=True
)

# Подключаем глобальные обработчики ошибок
#app.add_exception_handler(StarletteHTTPException, http_exception_handler)
#app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Подключаем все роутеры с общим префиксом /api/v1
app.include_router(books_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(attachments_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Library API"}