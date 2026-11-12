from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./local.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "sensor-corr-local-secret"
    jwt_algorithm: str = "HS256"
    access_expiry_minutes: int = 720
    project_key: str = "correlation_diag"
    seed_demo: bool = True

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
