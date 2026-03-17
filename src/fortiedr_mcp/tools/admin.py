"""Admin tools – system management, collector installers, licenses, mode."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all admin tools on the given FastMCP instance."""

    @mcp.tool()
    async def admin_list_collector_installers(
        organization: Optional[str] = None,
    ) -> Any:
        """List available FortiEDR collector installer packages.

        Returns the OS families and versions of collector installers available
        for download from this FortiEDR instance.

        Args:
            organization: Filter by organization name. Use exact name or leave
                None to get results for all organizations.
        """
        return await client.get(
            "/management-rest/admin/list-collector-installers",
            params={"organization": organization},
        )

    @mcp.tool()
    async def admin_list_system_summary(
        add_license_blob: Optional[bool] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Get a summary of the FortiEDR system health and status.

        Returns system-level information including collector counts, license
        status, component versions, and overall system health indicators.

        Args:
            add_license_blob: If True, includes the full license blob in the
                response.
            organization: Filter by organization name or None for all.
        """
        return await client.get(
            "/management-rest/admin/list-system-summary",
            params={
                "addLicenseBlob": add_license_blob,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def admin_ready() -> Any:
        """Check whether the FortiEDR system is ready to accept requests.

        A lightweight liveness probe – returns quickly with a status
        indicating whether the system has fully started.
        """
        return await client.get("/management-rest/admin/ready")

    @mcp.tool()
    async def admin_set_system_mode(
        mode: str,
        organization: Optional[str] = None,
        force_all: Optional[bool] = None,
    ) -> Any:
        """Switch the FortiEDR system operating mode (e.g., Simulation / Prevention).

        Args:
            mode: Target operating mode. Common values: 'Prevention',
                'Simulation'.
            organization: Organization to apply the mode change to. None
                applies to all organizations.
            force_all: If True, forces the mode change even on collectors
                that may not support it.
        """
        return await client.put(
            "/management-rest/admin/set-system-mode",
            params={
                "mode": mode,
                "organization": organization,
                "forceAll": force_all,
            },
        )

    @mcp.tool()
    async def admin_update_collector_installer(
        update_versions: str,
        collector_group_ids: Optional[str] = None,
        collector_groups: Optional[str] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Schedule a collector version upgrade for one or more collector groups.

        Triggers an update of the collector agent software to the specified
        version across the targeted collector groups.

        Args:
            update_versions: JSON string (or comma-separated) specifying the
                target versions per OS family.
            collector_group_ids: Comma-separated collector group IDs to update.
            collector_groups: Comma-separated collector group names to update.
            organization: Organization name or None for all.
        """
        return await client.post(
            "/management-rest/admin/update-collector-installer",
            params={
                "collectorGroupIds": collector_group_ids,
                "collectorGroups": collector_groups,
                "organization": organization,
            },
            json={"updateVersions": update_versions},
        )

    @mcp.tool()
    async def admin_upload_license(
        license_blob: str,
    ) -> Any:
        """Upload a new license to the FortiEDR instance.

        Args:
            license_blob: The license content as a Base64-encoded string,
                as provided by Fortinet.
        """
        return await client.put(
            "/management-rest/admin/upload-license",
            json={"licenseBlob": license_blob},
        )
