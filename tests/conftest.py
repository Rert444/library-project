import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app as fastapi_app
from app.db.base import Base
from app.db.session import get_session
import app.models # Важно для регистрации моделей в Base.metadata

# Используем SQLite в оперативной памяти для тестов (быстро и чисто)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Переопределяем зависимость get_session, чтобы FastAPI использовал тестовую БД
async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

# ВОТ ЗДЕСЬ НУЖНО БЫЛО ИСПРАВИТЬ (fastapi_app вместо app)
fastapi_app.dependency_overrides[get_session] = override_get_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    # Создаем таблицы перед тестами и удаляем после
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    # Клиент для запросов к API
    transport = ASGITransport(app=fastapi_app) # ВОТ ЗДЕСЬ ТОЖЕ fastapi_app
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def admin_token(client: AsyncClient) -> str:
    # Фикстура для получения токена администратора
    await client.post("/api/v1/auth/register", json={
        "email": "admin@test.com", "password": "password123", "role": "admin"
    })
    response = await client.post("/api/v1/auth/login", data={
        "username": "admin@test.com", "password": "password123"
    })
    return response.json()["access_token"]