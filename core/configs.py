from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    """
    Configurações gerais da aplicação
    """

    PROJECT_NAME: str = "tarefas_sql_offline"
    API_V1_STR: str = "/api/v1"
    DB_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/tarefas_sql_offline"
    )
    DBBaseModel: ClassVar[DeclarativeBase] = declarative_base()

    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    JWT_SECRET: str = "iDAkoOAjTQCB4DZ1asFZK0qqwjHDJBw2pbuozTCQpIk"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    class Config:
        case_sensitive = True


settings: Settings = Settings()
