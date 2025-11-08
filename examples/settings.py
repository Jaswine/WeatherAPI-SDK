
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    """
        Application settings loaded from env.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    OPENWEATHERMAP_API_KEY: str

settings = Settings()
