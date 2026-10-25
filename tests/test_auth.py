from httpx import AsyncClient


async def test_register_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "newuser@test.com", "password": "secret123", "role": "user"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@test.com"
    assert "password" not in response.json() # Пароль не должен возвращаться

async def test_register_invalid_data(client: AsyncClient):
    # Ошибка 422: невалидный email
    response = await client.post("/api/v1/auth/register", json={
        "email": "not-an-email", "password": "123"
    })
    assert response.status_code == 422