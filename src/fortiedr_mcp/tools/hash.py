"""Hash tools – search file hashes across events and threat-hunting data."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all hash tools on the given FastMCP instance."""

    @mcp.tool()
    async def hash_search(
        file_hashes: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Search for file hashes across FortiEDR events and the threat-hunting repository.

        Looks up one or more file hashes (MD5 or SHA256) and returns any
        matches found in security events or the threat-hunting data store,
        along with associated threat intelligence.

        Args:
            file_hashes: Comma-separated list of MD5 or SHA256 file hashes
                to search for.
            organization: Organization name or None for all organizations.
        """
        return await client.get(
            "/management-rest/hash/search",
            params={
                "fileHashes": file_hashes,
                "organization": organization,
            },
        )
