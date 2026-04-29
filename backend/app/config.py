"""Configuración de Flow desde variables de entorno."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "flow"
    debug: bool = False

    # Auth — REQUERIDO (sin default)
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 días

    # Database
    database_url: str = "sqlite+aiosqlite:///./flow.db"

    # MiniMax IA — REQUERIDO (sin default)
    minimax_api_key: str
    minimax_base_url: str = "https://api.minimax.chat/v1"

    # DeepSeek (razonamiento) — opcional
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"

    @classmethod
    def _validate_required(cls, v: str, field_name: str) -> str:
        """Valida que un campo requerido no esté vacío."""
        if not v or v.strip() == "":
            raise ValueError(
                f"{field_name} es requerido. "
                f"Configúralo vía variable de entorno o .env. "
                f"Ver Infisical: infisical run -- env=prod -- python ..."
            )
        return v


# Validación explícita al importar
try:
    settings = Settings()
except Exception as e:
    import sys
    print(f"ERROR de configuración: {e}", file=sys.stderr)
    print(
        "Asegúrate de que SECRET_KEY y MINIMAX_API_KEY estén definidas. "
        "Usa: infisical run --env=prod -- python -m uvicorn app.main:app",
        file=sys.stderr,
    )
    sys.exit(1)
