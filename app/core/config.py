from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Library API"
    app_debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./library.db"
    secret_key: str = "super_secret_key_change_me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Обязательно создаем экземпляр класса!
settings = Settings()