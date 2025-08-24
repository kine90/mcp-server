from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    MERAKI_API_KEY: str = ""
    # Selent integration removed
    CACHE_TTL_SECONDS: int = 300
    DISABLE_RESPONSE_CACHE: bool = False
    MCP_LOG_SECTIONS: bool = False
    # Mutation and surface controls
    ALLOW_MUTATIONS: bool = False
    REQUIRE_CONFIRM_FOR_MUTATIONS: bool = True
    ALLOW_SECTIONS: list[str] = []
    ALLOW_METHODS: list[str] = []  # format: section.method or just method
    DENY_SECTIONS: list[str] = []
    DENY_METHODS: list[str] = []   # format: section.method or just method
    # Guardrails
    MAX_PER_PAGE: int = 500
    MAX_TIMESPAN: int = 86400
    REDACT_KEYS: list[str] = [
        "psk",
        "password",
        "secret",
        "token",
        "apiKey",
        "key",
    ]
