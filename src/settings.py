from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPServerSettings(BaseSettings):
    """Pydantic settings model for MCP server settings."""

    model_config = SettingsConfigDict(
        env_prefix="SERVER_SETTINGS_",
        env_file=".env",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 8755


class MCPRunSettings(BaseSettings):
    """Pydantic settings model for MCP run settings."""

    model_config = SettingsConfigDict(
        env_prefix="RUN_SETTINGS_",
        env_file=".env",
        extra="ignore",
    )

    transport: Literal["stdio", "sse", "streamable-http"] = "stdio"


mcp_server_settings = MCPServerSettings()
mcp_run_settings = MCPRunSettings()
