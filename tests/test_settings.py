import os

from meraki_mcp.settings import ApiSettings


def test_settings_defaults_and_env(monkeypatch):
    # Ensure default API key is empty when not set
    monkeypatch.delenv("MERAKI_API_KEY", raising=False)
    defaults = ApiSettings()
    assert defaults.MERAKI_API_KEY == ""
    assert isinstance(defaults.REDACT_KEYS, list)
    assert {"password", "token", "apiKey"}.issubset(set(defaults.REDACT_KEYS))

    # Env override should populate value
    monkeypatch.setenv("MERAKI_API_KEY", "test_key")
    envset = ApiSettings()
    assert envset.MERAKI_API_KEY == "test_key"

