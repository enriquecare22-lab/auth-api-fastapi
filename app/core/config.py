import logging

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str
    # Seguridad
    SECRET_KEY: str = Field(min_length=32)
    ALGORITHM: str = Field(default="HS256")

    # Expiracion de tokens
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Configuracion interna de Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        # archivo .env
    )


class ConfigurationError(Exception):
    """Raised when application configuration is invalid."""


try:
    settings = Settings()

except ValidationError as error:
    logger.critical("Application configuration validation failed")

    invalid_fields = [
        {
            "fields": err["loc"][0],
            "message": err["msg"],
        }
        for err in error.errors()
    ]

    raise ConfigurationError(
        f"Invalid application configuration: {invalid_fields}"
    ) from error


# Instancia globlal
