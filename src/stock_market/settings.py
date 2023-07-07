from typing import Optional, Dict, Any
from stock_market.constants import DEFAULT_KEY_LENGTH, DEFAULT_STOCK_API_KEY
from pydantic import (
    BaseSettings,
    PostgresDsn,
    IPvAnyAddress,
    PositiveInt,
    validator,
    conint,
)


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    ROOT_PATH: str = ""
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    APP_MODULE: str = "stock_market.main:app"
    HOST: IPvAnyAddress = "0.0.0.0"
    PORT: PositiveInt = 8000
    API_KEY_LENGTH: conint(gt=0) = DEFAULT_KEY_LENGTH
    STOCK_API_KEY: str = DEFAULT_STOCK_API_KEY
    DEBUG_MODE: bool = False

    # Timezone
    DEFAULT_TIMEZONE: str = "Etc/UTC"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        """Assemble the database connection URL."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
