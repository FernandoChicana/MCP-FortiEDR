"""Threat Hunting Exclusions tools – manage threat-hunting data exclusion lists."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all threat-hunting exclusions tools on the given FastMCP instance."""

    @mcp.tool()
    async def th_exclusions_list_exclusion_lists(
        organization: Optional[str] = None,
    ) -> Any:
        """List all threat-hunting exclusion lists.

        Returns all named exclusion lists that filter out known-good events
        from the threat-hunting data repository.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/threat-hunting-exclusions/exclusions-list",
            params={"organization": organization},
        )

    @mcp.tool()
    async def th_exclusions_create_exclusion_list(
        name: str,
        organization: Optional[str] = None,
        collector_group_ids: Optional[str] = None,
    ) -> Any:
        """Create a new threat-hunting exclusion list.

        Args:
            name: Name for the new exclusion list.
            organization: Organization name or None for all.
            collector_group_ids: Comma-separated collector group IDs to
                associate with this exclusion list.
        """
        return await client.post(
            "/management-rest/threat-hunting-exclusions/exclusions-list",
            json={
                "name": name,
                "organization": organization,
                "collectorGroupIds": collector_group_ids,
            },
        )

    @mcp.tool()
    async def th_exclusions_update_exclusion_list(
        list_name: str,
        organization: Optional[str] = None,
        new_name: Optional[str] = None,
        collector_group_ids: Optional[str] = None,
    ) -> Any:
        """Update an existing threat-hunting exclusion list.

        Args:
            list_name: Current name of the exclusion list to update.
            organization: Organization name or None for all.
            new_name: New name for the exclusion list (if renaming).
            collector_group_ids: New comma-separated collector group IDs.
        """
        return await client.put(
            "/management-rest/threat-hunting-exclusions/exclusions-list",
            json={
                "listName": list_name,
                "organization": organization,
                "newName": new_name,
                "collectorGroupIds": collector_group_ids,
            },
        )

    @mcp.tool()
    async def th_exclusions_delete_exclusion_list(
        list_name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Delete a threat-hunting exclusion list.

        Args:
            list_name: Name of the exclusion list to delete.
            organization: Organization name or None for all.
        """
        return await client.delete(
            "/management-rest/threat-hunting-exclusions/exclusions-list",
            params={"listName": list_name, "organization": organization},
        )

    @mcp.tool()
    async def th_exclusions_add_exclusions(
        exclusion_list_name: str,
        exclusions: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Add exclusion entries to a threat-hunting exclusion list.

        Args:
            exclusion_list_name: Name of the target exclusion list.
            exclusions: JSON string containing the exclusion entries
                (field/value pairs to exclude from threat-hunting queries).
            organization: Organization name or None for all.
        """
        return await client.post(
            "/management-rest/threat-hunting-exclusions/exclusion",
            json={
                "exclusionListName": exclusion_list_name,
                "exclusions": exclusions,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def th_exclusions_update_exclusions(
        exclusion_list_name: str,
        exclusions: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Update existing exclusion entries in a threat-hunting exclusion list.

        Args:
            exclusion_list_name: Name of the exclusion list to update.
            exclusions: JSON string containing updated exclusion entries.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/threat-hunting-exclusions/exclusion",
            json={
                "exclusionListName": exclusion_list_name,
                "exclusions": exclusions,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def th_exclusions_delete_exclusions(
        exclusion_ids: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Delete specific exclusion entries from a threat-hunting exclusion list.

        Args:
            exclusion_ids: Comma-separated IDs of the exclusion entries to delete.
            organization: Organization name or None for all.
        """
        return await client.delete(
            "/management-rest/threat-hunting-exclusions/exclusion",
            json={
                "exclusionIds": exclusion_ids,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def th_exclusions_get_metadata() -> Any:
        """Get metadata describing available properties for exclusion configuration.

        Returns the schema of fields available for building threat-hunting
        exclusion rules, including valid operators and value types.
        """
        return await client.get(
            "/management-rest/threat-hunting-exclusions/exclusions-metadata"
        )

    @mcp.tool()
    async def th_exclusions_search(
        organization: Optional[str] = None,
        search_text: Optional[str] = None,
        os: Optional[str] = None,
    ) -> Any:
        """Search for threat-hunting exclusion entries by text and OS.

        Args:
            organization: Organization name or None for all.
            search_text: Free-text search term to find matching exclusions.
            os: Operating system filter (e.g., 'Windows', 'Linux').
        """
        return await client.get(
            "/management-rest/threat-hunting-exclusions/exclusions-search",
            params={
                "organization": organization,
                "searchText": search_text,
                "os": os,
            },
        )
