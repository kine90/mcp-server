from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    MERAKI_API_KEY: str = ""
    # Selent integration removed
    CACHE_TTL_SECONDS: int = 300
    DISABLE_RESPONSE_CACHE: bool = False
    MCP_LOG_SECTIONS: bool = False
    REDACT_KEYS: list[str] = [
        "psk",
        "password",
        "secret",
        "token",
        "apiKey",
        "key",
    ]
