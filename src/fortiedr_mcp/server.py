"""FortiEDR MCP Server entry point.

Starts a FastMCP server exposing all FortiEDR REST API endpoints as tools,
plus a /health HTTP endpoint for container health checks.

Transport: streamable-http (compatible with Claude Desktop and any MCP client).
Port: controlled by MCP_SERVER_PORT environment variable (default 8000).
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

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
# /health endpoint
# ---------------------------------------------------------------------------

async def health_handler(request: Request) -> JSONResponse:
    """Liveness + readiness probe that also verifies FortiEDR connectivity."""
    connected = await client.check_connectivity()
    status_code = 200 if connected else 503
    return JSONResponse(
        {
            "status": "ok" if connected else "degraded",
            "host": settings.fortiedr_host,
            "port": settings.fortiedr_port,
            "fortiedr_connected": connected,
        },
        status_code=status_code,
    )

# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    logger.info(
        "Starting mcp-fortiedr → FortiEDR at %s:%s",
        settings.fortiedr_host,
        settings.fortiedr_port,
    )
    try:
        yield
    finally:
        logger.info("Shutting down – closing HTTP client session")
        await client.close()

# ---------------------------------------------------------------------------
# Combined ASGI application
# ---------------------------------------------------------------------------
# FastMCP 2.x exposes http_app() which returns a Starlette ASGI app.
# We wrap it alongside the /health route in a parent Starlette application.

def create_app() -> Starlette:
    mcp_asgi = mcp.http_app(path="/")

    return Starlette(
        routes=[
            Route("/health", endpoint=health_handler, methods=["GET"]),
            Mount("/", app=mcp_asgi),
        ],
        lifespan=lifespan,
    )


app = create_app()

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server with uvicorn."""
    logger.info(
        "mcp-fortiedr starting on port %d (log level: %s)",
        settings.mcp_server_port,
        settings.log_level,
    )
    uvicorn.run(
        "fortiedr_mcp.server:app",
        host="0.0.0.0",
        port=settings.mcp_server_port,
        log_level=settings.log_level.lower(),
        access_log=True,
    )


if __name__ == "__main__":
    main()
