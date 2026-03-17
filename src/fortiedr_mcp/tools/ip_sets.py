"""IP Sets tools – manage named IP address sets used in policies."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all IP sets tools on the given FastMCP instance."""

    @mcp.tool()
    async def ip_sets_list(
        organization: Optional[str] = None,
        ip: Optional[str] = None,
    ) -> Any:
        """List named IP sets defined in FortiEDR.

        Returns all IP sets with their included/excluded IP ranges,
        used in communication control and other policies.

        Args:
            organization: Organization name or None for all.
            ip: Filter to only sets that contain this IP address.
        """
        return await client.get(
            "/management-rest/ip-sets/list-ip-sets",
            params={"organization": organization, "ip": ip},
        )

    @mcp.tool()
    async def ip_sets_create(
        name: str,
        include: str,
        organization: Optional[str] = None,
        description: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Any:
        """Create a new named IP set in FortiEDR.

        IP sets are reusable groups of IP addresses/ranges used as targets
        in communication control policies and other rule definitions.

        Args:
            name: Unique name for the IP set.
            include: Comma-separated IP addresses or CIDR ranges to include
                (e.g., '192.168.1.0/24,10.0.0.1').
            organization: Organization to create the IP set in.
            description: Optional description of the IP set's purpose.
            exclude: Comma-separated IP addresses or CIDR ranges to exclude
                from the included ranges.
        """
        return await client.post(
            "/management-rest/ip-sets/create-ip-set",
            json={
                "name": name,
                "include": include,
                "organization": organization,
                "description": description,
                "exclude": exclude,
            },
        )

    @mcp.tool()
    async def ip_sets_update(
        name: str,
        include: str,
        organization: Optional[str] = None,
        description: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Any:
        """Update an existing named IP set in FortiEDR.

        Args:
            name: Name of the IP set to update.
            include: New comma-separated IP addresses or CIDR ranges to include.
            organization: Organization name or None for all.
            description: Updated description.
            exclude: New comma-separated exclusion IP ranges.
        """
        return await client.put(
            "/management-rest/ip-sets/update-ip-set",
            params={"organization": organization},
            json={
                "name": name,
                "include": include,
                "description": description,
                "exclude": exclude,
            },
        )

    @mcp.tool()
    async def ip_sets_delete(
        ip_sets: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Delete one or more named IP sets from FortiEDR.

        Args:
            ip_sets: Comma-separated names of IP sets to delete.
            organization: Organization name or None for all.
        """
        return await client.delete(
            "/management-rest/ip-sets/delete-ip-set",
            params={"ipSets": ip_sets, "organization": organization},
        )
