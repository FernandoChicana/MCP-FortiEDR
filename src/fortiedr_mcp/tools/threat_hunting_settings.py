"""Threat Hunting Settings tools – manage threat-hunting profiles and configuration."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all threat-hunting settings tools on the given FastMCP instance."""

    @mcp.tool()
    async def th_settings_get_metadata() -> Any:
        """Get threat-hunting settings metadata.

        Returns the available configuration categories, data types, and
        telemetry settings available for threat-hunting profiles.
        """
        return await client.get(
            "/management-rest/threat-hunting-settings/threat-hunting-metadata"
        )

    @mcp.tool()
    async def th_settings_list_profiles(
        organization: Optional[str] = None,
    ) -> Any:
        """List all threat-hunting profiles.

        Returns profiles that define what telemetry categories are collected
        for the threat-hunting repository.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/threat-hunting-settings/threat-hunting-profile",
            params={"organization": organization},
        )

    @mcp.tool()
    async def th_settings_create_or_update_profile(
        name: str,
        organization: Optional[str] = None,
        new_name: Optional[str] = None,
        associated_collector_group_ids: Optional[str] = None,
        threat_hunting_category_list: Optional[str] = None,
    ) -> Any:
        """Create or update a threat-hunting telemetry collection profile.

        Profiles determine which telemetry categories (process creation,
        network connections, file operations, etc.) are captured for
        the threat-hunting repository.

        Args:
            name: Name of the profile to create or update.
            organization: Organization name or None for all.
            new_name: New name for the profile (if renaming an existing one).
            associated_collector_group_ids: Comma-separated collector group IDs
                to associate with this profile.
            threat_hunting_category_list: JSON string defining which telemetry
                categories to enable in this profile.
        """
        return await client.post(
            "/management-rest/threat-hunting-settings/threat-hunting-profile",
            json={
                "name": name,
                "organization": organization,
                "newName": new_name,
                "associatedCollectorGroupIds": associated_collector_group_ids,
                "threatHuntingCategoryList": threat_hunting_category_list,
            },
        )

    @mcp.tool()
    async def th_settings_delete_profile(
        name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Delete a threat-hunting telemetry collection profile.

        Args:
            name: Name of the profile to delete.
            organization: Organization name or None for all.
        """
        return await client.delete(
            "/management-rest/threat-hunting-settings/threat-hunting-profile",
            params={"name": name, "organization": organization},
        )

    @mcp.tool()
    async def th_settings_assign_collector_groups_to_profile(
        name: str,
        associated_collector_group_ids: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Assign collector groups to a threat-hunting profile.

        Args:
            name: Name of the threat-hunting profile.
            associated_collector_group_ids: Comma-separated collector group IDs
                to assign to this profile.
            organization: Organization name or None for all.
        """
        return await client.post(
            "/management-rest/threat-hunting-settings/threat-hunting-profile/collector-groups",
            json={
                "name": name,
                "associatedCollectorGroupIds": associated_collector_group_ids,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def th_settings_clone_profile(
        existing_profile_name: str,
        clone_profile_name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Clone an existing threat-hunting profile under a new name.

        Args:
            existing_profile_name: Name of the profile to clone.
            clone_profile_name: Name for the new cloned profile.
            organization: Organization name or None for all.
        """
        return await client.post(
            "/management-rest/threat-hunting-settings/threat-hunting-profile-clone",
            params={
                "existingProfileName": existing_profile_name,
                "cloneProfileName": clone_profile_name,
                "organization": organization,
            },
        )
