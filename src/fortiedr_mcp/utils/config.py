"""Configuration management via environment variables using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """FortiEDR MCP server configuration.

    All values are read from environment variables (or .env file).
    Each deployed container has its own .env pointing to a specific FortiEDR instance.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    fortiedr_host: str
    fortiedr_user: str
    fortiedr_password: str
    fortiedr_port: int = 443
    fortiedr_verify_ssl: bool = False
    mcp_server_port: int = 8000
    log_level: str = "INFO"


settings = Settings()
