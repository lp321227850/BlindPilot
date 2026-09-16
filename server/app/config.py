from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    env: str = Field(default="development", validation_alias=AliasChoices("BLINDPILOT_ENV", "ENV"))
    public_url: str = Field(
        default="http://127.0.0.1:8080",
        validation_alias=AliasChoices("BLINDPILOT_PUBLIC_URL", "PUBLIC_URL"),
    )
    database_url: str = Field(
        default="sqlite+pysqlite:///:memory:",
        validation_alias=AliasChoices("BLINDPILOT_DATABASE_URL", "DATABASE_URL"),
    )
    pairing_secret: str = Field(
        default="dev-only-change-me",
        validation_alias=AliasChoices("BLINDPILOT_PAIRING_SECRET", "PAIRING_SECRET"),
    )
    agent_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("BLINDPILOT_AGENT_API_KEY", "AGENT_API_KEY"),
    )
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("BLINDPILOT_LOG_LEVEL", "LOG_LEVEL"))
    host: str = "127.0.0.1"
    port: int = 8080

    @property
    def agent_configured(self) -> bool:
        return bool(self.agent_api_key.strip())


settings = Settings()
