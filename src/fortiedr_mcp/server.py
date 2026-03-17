"""FortiEDR MCP Server entry point.

Starts a FastMCP server exposing all FortiEDR REST API endpoints as tools,
plus a /health HTTP endpoint for container health checks.

Transport: streamable-http (compatible with any MCP client).
Port: controlled by MCP_SERVER_PORT environment variable (default 8000).
"""

import logging
import sys

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .api.client import client
from .tools import register_all
from .utils.config import settings

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# FastMCP instance
# ---------------------------------------------------------------------------
mcp = FastMCP(
    name="mcp-fortiedr",
    instructions=(
        "MCP server that wraps the Fortinet FortiEDR REST API. "
        "Use these tools to manage security events, collectors, policies, "
        "threat hunting, forensics, and more on a FortiEDR instance. "
        f"Connected to FortiEDR host: {settings.fortiedr_host}:{settings.fortiedr_port}."
    ),
)

# Register all tool categories
register_all(mcp)
logger.info("Registered all FortiEDR tool categories")

# ---------------------------------------------------------------------------
# /health endpoint via FastMCP custom route
# ---------------------------------------------------------------------------

@mcp.custom_route("/health", methods=["GET"])
async def health_handler(request: Request) -> JSONResponse:
    """Liveness + readiness probe that also verifies FortiEDR connectivity."""
    connected = await client.check_connectivity()
    return JSONResponse(
        {
            "status": "ok" if connected else "degraded",
            "host": settings.fortiedr_host,
            "port": settings.fortiedr_port,
            "fortiedr_connected": connected,
        },
        status_code=200 if connected else 503,
    )

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server via FastMCP's built-in transport."""
    logger.info(
        "mcp-fortiedr starting on port %d (log level: %s)",
        settings.mcp_server_port,
        settings.log_level,
    )
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=settings.mcp_server_port,
    )


if __name__ == "__main__":
    main()
