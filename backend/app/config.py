"""Configuración de Flow desde variables de entorno."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "flow"
    debug: bool = False

    # Auth
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 días

    # Database
    database_url: str = "sqlite+aiosqlite:///./flow.db"

    # MiniMax IA
    minimax_api_key: str = ""
    minimax_base_url: str = "https://api.minimax.chat/v1"

    # DeepSeek (razonamiento)
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"


settings = Settings()
