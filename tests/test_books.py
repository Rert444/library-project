from httpx import AsyncClient


async def test_create_book_unauthorized(client: AsyncClient):
    # Ошибка 401: без токена
    response = await client.post("/api/v1/books/", json={"title": "Книга"})
    assert response.status_code == 401


async def test_create_book_forbidden(client: AsyncClient):
    # Ошибка 403: пользователь с ролью user не может создавать книги
    await client.post("/api/v1/auth/register", json={
        "email": "user@test.com", "password": "secret123", "role": "user"
    })
    login_resp = await client.post("/api/v1/auth/login", data={
        "username": "user@test.com", "password": "secret123"
    })
    token = login_resp.json()["access_token"]

    response = await client.post(
        "/api/v1/books/",
        json={"title": "Книга", "author_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


async def test_create_and_get_book(client: AsyncClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Создаем автора (используем наш временный маршрут)
    author_resp = await client.post("/api/v1/books/authors/?name=Пушкин", headers=headers)
    author_id = author_resp.json()["id"]

    # 2. Создаем книгу (Ожидаем 201)
    response = await client.post("/api/v1/books/", json={
        "title": "Евгений Онегин",
        "author_id": author_id,
        "genre": "Роман",
        "year": 1833,
        "copies_total": 5
    }, headers=headers)

    assert response.status_code == 201
    book_id = response.json()["id"]

    # 3. Получаем книгу по ID (Ожидаем 200)
    get_resp = await client.get(f"/api/v1/books/{book_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Евгений Онегин"

    # 4. Ошибка 404 (несуществующая книга)
    error_resp = await client.get("/api/v1/books/9999")
    assert error_resp.status_code == 404