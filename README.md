# Library API (FastAPI)

Учебный проект по веб-программированию на FastAPI (Вариант «Библиотека»).

## Описание
Сервис предоставляет REST API для управления библиотекой. Реализованы CRUD-операции для книг, авторов, JWT-аутентификация, роли (admin, manager, user), загрузка файлов и тесты.

## Технологии
- Python 3.12
- FastAPI
- SQLAlchemy (async)
- Alembic
- SQLite
- Docker, Docker Compose
- Pytest, Ruff

## Запуск проекта (Docker)
1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd <project-directory>