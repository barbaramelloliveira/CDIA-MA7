from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # 👈 aqui está a correção

class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool
    max_mesas: int
    max_pessoas_por_mesa: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

settings = Settings()