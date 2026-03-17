"""Inventory tools – collectors, cores, aggregators, and unmanaged devices."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all inventory tools on the given FastMCP instance."""

    @mcp.tool()
    async def inventory_list_collectors(
        organization: Optional[str] = None,
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        ips: Optional[str] = None,
        states: Optional[str] = None,
        collector_groups: Optional[str] = None,
        operating_systems: Optional[str] = None,
        os_families: Optional[str] = None,
        versions: Optional[str] = None,
        logged_user: Optional[str] = None,
        first_seen: Optional[str] = None,
        last_seen_start: Optional[str] = None,
        last_seen_end: Optional[str] = None,
        has_crash_dumps: Optional[bool] = None,
        show_expired: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """List FortiEDR collector agents installed on endpoints.

        Returns a paginated list of collector agents with their status,
        version, OS information, and group assignments.

        Args:
            organization: Organization name or None for all.
            devices: Comma-separated device hostnames to filter.
            devices_ids: Comma-separated device IDs to filter.
            ips: Comma-separated IP addresses to filter.
            states: Comma-separated collector states
                (e.g., 'Running', 'Disconnected', 'Disabled').
            collector_groups: Comma-separated collector group names.
            operating_systems: Comma-separated OS names.
            os_families: Comma-separated OS families (Windows, Linux, macOS).
            versions: Comma-separated collector version strings.
            logged_user: Filter by the currently logged-in username.
            first_seen: ISO-8601 – show collectors first seen after this date.
            last_seen_start: ISO-8601 start for last-seen filter.
            last_seen_end: ISO-8601 end for last-seen filter.
            has_crash_dumps: If True, show only collectors with crash dumps.
            show_expired: If True, include expired (old) collector records.
            strict_mode: Use exact matching for string filters.
            items_per_page: Results per page.
            page_number: Page number (1-based).
            sorting: Sort expression, e.g. 'lastSeen desc'.
        """
        return await client.get(
            "/management-rest/inventory/list-collectors",
            params={
                "organization": organization,
                "devices": devices,
                "devicesIds": devices_ids,
                "ips": ips,
                "states": states,
                "collectorGroups": collector_groups,
                "operatingSystems": operating_systems,
                "osFamilies": os_families,
                "versions": versions,
                "loggedUser": logged_user,
                "firstSeen": first_seen,
                "lastSeenStart": last_seen_start,
                "lastSeenEnd": last_seen_end,
                "hasCrashDumps": has_crash_dumps,
                "showExpired": show_expired,
                "strictMode": strict_mode,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def inventory_list_collector_groups(
        organization: Optional[str] = None,
    ) -> Any:
        """List all collector groups defined in FortiEDR.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/inventory/list-collector-groups",
            params={"organization": organization},
        )

    @mcp.tool()
    async def inventory_create_collector_group(
        name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Create a new collector group for organizing endpoint agents.

        Args:
            name: Name for the new collector group.
            organization: Organization to create the group in.
        """
        return await client.post(
            "/management-rest/inventory/create-collector-group",
            params={"name": name, "organization": organization},
        )

    @mcp.tool()
    async def inventory_move_collectors(
        collectors: str,
        target_collector_group: str,
        organization: Optional[str] = None,
        force_assign: Optional[bool] = None,
    ) -> Any:
        """Move one or more collector agents to a different collector group.

        Args:
            collectors: Comma-separated collector hostnames to move.
            target_collector_group: Name of the destination collector group.
            organization: Organization name or None for all.
            force_assign: If True, force the move even if policy conflicts exist.
        """
        return await client.put(
            "/management-rest/inventory/move-collectors",
            params={
                "collectors": collectors,
                "targetCollectorGroup": target_collector_group,
                "organization": organization,
                "forceAssign": force_assign,
            },
        )

    @mcp.tool()
    async def inventory_toggle_collectors(
        enable: bool,
        organization: Optional[str] = None,
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        collector_groups: Optional[str] = None,
        ips: Optional[str] = None,
        states: Optional[str] = None,
        operating_systems: Optional[str] = None,
        os_families: Optional[str] = None,
        versions: Optional[str] = None,
        logged_user: Optional[str] = None,
        first_seen: Optional[str] = None,
        last_seen_start: Optional[str] = None,
        last_seen_end: Optional[str] = None,
        has_crash_dumps: Optional[bool] = None,
        show_expired: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Enable or disable collector agents matching the filter criteria.

        Args:
            enable: True to enable collectors, False to disable.
            organization: Organization name or None for all.
            devices: Comma-separated device hostnames.
            devices_ids: Comma-separated device IDs.
            collector_groups: Comma-separated collector group names.
            ips: Comma-separated IP addresses.
            states: Current collector states to filter by.
            operating_systems: OS names to filter by.
            os_families: OS families to filter by.
            versions: Collector versions to filter by.
            logged_user: Username filter.
            first_seen: ISO-8601 first-seen date filter.
            last_seen_start: ISO-8601 last-seen start.
            last_seen_end: ISO-8601 last-seen end.
            has_crash_dumps: Filter by crash dump presence.
            show_expired: Include expired collector records.
            strict_mode: Use exact matching.
            items_per_page: Results per page.
            page_number: Page number.
            sorting: Sort expression.
        """
        return await client.put(
            "/management-rest/inventory/toggle-collectors",
            params={
                "enable": enable,
                "organization": organization,
                "devices": devices,
                "devicesIds": devices_ids,
                "collectorGroups": collector_groups,
                "ips": ips,
                "states": states,
                "operatingSystems": operating_systems,
                "osFamilies": os_families,
                "versions": versions,
                "loggedUser": logged_user,
                "firstSeen": first_seen,
                "lastSeenStart": last_seen_start,
                "lastSeenEnd": last_seen_end,
                "hasCrashDumps": has_crash_dumps,
                "showExpired": show_expired,
                "strictMode": strict_mode,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def inventory_isolate_collectors(
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Isolate one or more devices from the network via their FortiEDR collector.

        Network isolation cuts off all network communication except the
        FortiEDR management channel, effectively quarantining the device.

        Args:
            devices: Comma-separated device hostnames to isolate.
            devices_ids: Comma-separated device IDs to isolate.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/inventory/isolate-collectors",
            params={
                "devices": devices,
                "devicesIds": devices_ids,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def inventory_unisolate_collectors(
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Remove network isolation from one or more devices.

        Restores full network access to devices previously isolated
        via FortiEDR.

        Args:
            devices: Comma-separated device hostnames to unisolate.
            devices_ids: Comma-separated device IDs to unisolate.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/inventory/unisolate-collectors",
            params={
                "devices": devices,
                "devicesIds": devices_ids,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def inventory_delete_collectors(
        organization: Optional[str] = None,
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        collector_groups: Optional[str] = None,
        ips: Optional[str] = None,
        states: Optional[str] = None,
        operating_systems: Optional[str] = None,
        os_families: Optional[str] = None,
        versions: Optional[str] = None,
        logged_user: Optional[str] = None,
        first_seen: Optional[str] = None,
        last_seen_start: Optional[str] = None,
        last_seen_end: Optional[str] = None,
        has_crash_dumps: Optional[bool] = None,
        show_expired: Optional[bool] = None,
        confirm_deletion: Optional[bool] = None,
        delete_all: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Delete collector agent records matching the filter criteria.

        WARNING: This removes the collector records from FortiEDR. It does not
        uninstall the agent software from the endpoint.

        Args:
            organization: Organization name or None for all.
            devices: Comma-separated device hostnames.
            devices_ids: Comma-separated device IDs.
            collector_groups: Comma-separated collector group names.
            ips: Comma-separated IP addresses.
            states: Collector states to filter by.
            operating_systems: OS names to filter by.
            os_families: OS families to filter by.
            versions: Collector versions to filter by.
            logged_user: Username filter.
            first_seen: First-seen date filter (ISO-8601).
            last_seen_start: Last-seen start filter (ISO-8601).
            last_seen_end: Last-seen end filter (ISO-8601).
            has_crash_dumps: Filter by crash dump presence.
            show_expired: Include expired records.
            confirm_deletion: Must be True to confirm the deletion.
            delete_all: If True, delete all matching records.
            strict_mode: Use exact matching.
            items_per_page: Results per page.
            page_number: Page number.
            sorting: Sort expression.
        """
        return await client.delete(
            "/management-rest/inventory/delete-collectors",
            params={
                "organization": organization,
                "devices": devices,
                "devicesIds": devices_ids,
                "collectorGroups": collector_groups,
                "ips": ips,
                "states": states,
                "operatingSystems": operating_systems,
                "osFamilies": os_families,
                "versions": versions,
                "loggedUser": logged_user,
                "firstSeen": first_seen,
                "lastSeenStart": last_seen_start,
                "lastSeenEnd": last_seen_end,
                "hasCrashDumps": has_crash_dumps,
                "showExpired": show_expired,
                "confirmDeletion": confirm_deletion,
                "deleteAll": delete_all,
                "strictMode": strict_mode,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def inventory_list_cores(
        organization: Optional[str] = None,
        names: Optional[str] = None,
        ip: Optional[str] = None,
        versions: Optional[str] = None,
        deployment_modes: Optional[str] = None,
        has_crash_dumps: Optional[bool] = None,
    ) -> Any:
        """List FortiEDR core components (detection engines).

        Returns status, version, IP, and deployment mode for each core.

        Args:
            organization: Organization name or None for all.
            names: Comma-separated core names to filter.
            ip: IP address filter.
            versions: Comma-separated version strings.
            deployment_modes: Deployment modes to filter by.
            has_crash_dumps: If True, show only cores with crash dumps.
        """
        return await client.get(
            "/management-rest/inventory/list-cores",
            params={
                "organization": organization,
                "names": names,
                "ip": ip,
                "versions": versions,
                "deploymentModes": deployment_modes,
                "hasCrashDumps": has_crash_dumps,
            },
        )

    @mcp.tool()
    async def inventory_list_aggregators(
        organization: Optional[str] = None,
        names: Optional[str] = None,
        ip: Optional[str] = None,
        versions: Optional[str] = None,
    ) -> Any:
        """List FortiEDR aggregator components.

        Returns aggregator status, version, and connectivity information.

        Args:
            organization: Organization name or None for all.
            names: Comma-separated aggregator names.
            ip: IP address filter.
            versions: Comma-separated version strings.
        """
        return await client.get(
            "/management-rest/inventory/list-aggregators",
            params={
                "organization": organization,
                "names": names,
                "ip": ip,
                "versions": versions,
            },
        )

    @mcp.tool()
    async def inventory_list_repositories() -> Any:
        """List FortiEDR repository (EDR) components.

        Returns information about the data repository nodes used for
        storing threat-hunting and forensic data.
        """
        return await client.get("/management-rest/inventory/list-repositories")

    @mcp.tool()
    async def inventory_list_unmanaged_devices(
        organization: Optional[str] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """List network devices discovered by FortiEDR that have no collector installed.

        Returns devices detected via network scanning that are not yet
        protected by FortiEDR collectors.

        Args:
            organization: Organization name or None for all.
            strict_mode: Use exact matching for string filters.
            items_per_page: Results per page.
            page_number: Page number (1-based).
            sorting: Sort expression.
        """
        return await client.get(
            "/management-rest/inventory/list-unmanaged-devices",
            params={
                "organization": organization,
                "strictMode": strict_mode,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def inventory_system_logs() -> Any:
        """Retrieve FortiEDR system diagnostic logs.

        Downloads the current system log bundle for troubleshooting
        platform-level issues.
        """
        return await client.get("/management-rest/inventory/system-logs")

    @mcp.tool()
    async def inventory_collector_logs(
        device: Optional[str] = None,
        device_id: Optional[int] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Download diagnostic logs from a specific collector agent.

        Args:
            device: Hostname of the device whose collector logs to retrieve.
            device_id: Numeric device ID (alternative to hostname).
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/inventory/collector-logs",
            params={
                "device": device,
                "deviceId": device_id,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def inventory_core_logs(
        device: Optional[str] = None,
        device_id: Optional[int] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Download diagnostic logs from a specific FortiEDR core component.

        Args:
            device: Hostname of the core device.
            device_id: Numeric device ID.
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/inventory/core-logs",
            params={
                "device": device,
                "deviceId": device_id,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def inventory_aggregator_logs(
        device: Optional[str] = None,
        device_id: Optional[int] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Download diagnostic logs from a specific FortiEDR aggregator.

        Args:
            device: Hostname of the aggregator device.
            device_id: Numeric device ID.
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/inventory/aggregator-logs",
            params={
                "device": device,
                "deviceId": device_id,
                "organization": organization,
            },
        )
