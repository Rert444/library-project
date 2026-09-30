from fastapi import FastAPI
from app.api.v1.book import router as books_router

app = FastAPI(title="Library API", version="1.0.0")

# Подключаем маршруты с префиксом версии API
app.include_router(books_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to Library API"}