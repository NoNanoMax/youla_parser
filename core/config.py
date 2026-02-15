from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    API_PREFIX: str = "/api/v1"

    HEADLESS: bool = True
    NAV_TIMEOUT_MS: int = 20_000
    MAX_CONCURRENCY: int = 5
    CACHE_TTL_SEC: int = 120

settings = Settings()

