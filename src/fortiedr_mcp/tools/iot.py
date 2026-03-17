"""IoT tools – manage IoT device inventory and groups."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)

# Shared IoT filter param builder
def _iot_filter(
    organization: Optional[str],
    devices: Optional[str],
    devices_ids: Optional[str],
    iot_groups: Optional[str],
    iot_groups_ids: Optional[str],
    categories: Optional[str],
    vendors: Optional[str],
    models: Optional[str],
    locations: Optional[str],
    internal_ips: Optional[str],
    mac_addresses: Optional[str],
    first_seen_start: Optional[str],
    first_seen_end: Optional[str],
    last_seen_start: Optional[str],
    last_seen_end: Optional[str],
    show_expired: Optional[bool],
    strict_mode: Optional[bool],
    items_per_page: Optional[int],
    page_number: Optional[int],
    sorting: Optional[str],
) -> dict:
    return {
        "organization": organization,
        "devices": devices,
        "devicesIds": devices_ids,
        "iotGroups": iot_groups,
        "iotGroupsIds": iot_groups_ids,
        "categories": categories,
        "vendors": vendors,
        "models": models,
        "locations": locations,
        "internalIps": internal_ips,
        "macAddresses": mac_addresses,
        "firstSeenStart": first_seen_start,
        "firstSeenEnd": first_seen_end,
        "lastSeenStart": last_seen_start,
        "lastSeenEnd": last_seen_end,
        "showExpired": show_expired,
        "strictMode": strict_mode,
        "itemsPerPage": items_per_page,
        "pageNumber": page_number,
        "sorting": sorting,
    }


def register(mcp: FastMCP) -> None:
    """Register all IoT tools on the given FastMCP instance."""

    @mcp.tool()
    async def iot_list_iot_devices(
        organization: Optional[str] = None,
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        iot_groups: Optional[str] = None,
        iot_groups_ids: Optional[str] = None,
        categories: Optional[str] = None,
        vendors: Optional[str] = None,
        models: Optional[str] = None,
        locations: Optional[str] = None,
        internal_ips: Optional[str] = None,
        mac_addresses: Optional[str] = None,
        first_seen_start: Optional[str] = None,
        first_seen_end: Optional[str] = None,
        last_seen_start: Optional[str] = None,
        last_seen_end: Optional[str] = None,
        show_expired: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """List IoT devices discovered in the network by FortiEDR.

        Returns IoT/OT devices with their classification, vendor, model,
        network information, and group assignments.

        Args:
            organization: Organization name or None for all.
            devices: Comma-separated device names.
            devices_ids: Comma-separated device IDs.
            iot_groups: Comma-separated IoT group names.
            iot_groups_ids: Comma-separated IoT group IDs.
            categories: Comma-separated device categories
                (e.g., 'Camera', 'Printer', 'Industrial').
            vendors: Comma-separated vendor names.
            models: Comma-separated model names.
            locations: Comma-separated location names.
            internal_ips: Comma-separated internal IP addresses.
            mac_addresses: Comma-separated MAC addresses.
            first_seen_start: ISO-8601 start for first-seen filter.
            first_seen_end: ISO-8601 end for first-seen filter.
            last_seen_start: ISO-8601 start for last-seen filter.
            last_seen_end: ISO-8601 end for last-seen filter.
            show_expired: Include expired/inactive device records.
            strict_mode: Use exact matching for string filters.
            items_per_page: Results per page.
            page_number: Page number (1-based).
            sorting: Sort expression.
        """
        return await client.get(
            "/management-rest/iot/list-iot-devices",
            params=_iot_filter(
                organization=organization, devices=devices,
                devices_ids=devices_ids, iot_groups=iot_groups,
                iot_groups_ids=iot_groups_ids, categories=categories,
                vendors=vendors, models=models, locations=locations,
                internal_ips=internal_ips, mac_addresses=mac_addresses,
                first_seen_start=first_seen_start,
                first_seen_end=first_seen_end,
                last_seen_start=last_seen_start, last_seen_end=last_seen_end,
                show_expired=show_expired, strict_mode=strict_mode,
                items_per_page=items_per_page, page_number=page_number,
                sorting=sorting,
            ),
        )

    @mcp.tool()
    async def iot_list_iot_groups(
        organization: Optional[str] = None,
    ) -> Any:
        """List all IoT device groups defined in FortiEDR.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/iot/list-iot-groups",
            params={"organization": organization},
        )

    @mcp.tool()
    async def iot_create_iot_group(
        name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Create a new IoT device group for organizing IoT inventory.

        Args:
            name: Name for the new IoT group.
            organization: Organization to create the group in.
        """
        return await client.post(
            "/management-rest/iot/create-iot-group",
            params={"name": name, "organization": organization},
        )

    @mcp.tool()
    async def iot_move_iot_devices(
        iot_device_ids: str,
        target_iot_group: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Move IoT devices to a different IoT group.

        Args:
            iot_device_ids: Comma-separated IoT device IDs to move.
            target_iot_group: Name of the destination IoT group.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/iot/move-iot-devices",
            params={
                "iotDeviceIds": iot_device_ids,
                "targetIotGroup": target_iot_group,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def iot_export_iot_json(
        iot_device_ids: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Export IoT device records as JSON for external processing.

        Args:
            iot_device_ids: Comma-separated IoT device IDs to export.
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/iot/export-iot-json",
            params={
                "iotDeviceIds": iot_device_ids,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def iot_rescan_iot_device_details(
        organization: Optional[str] = None,
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        iot_groups: Optional[str] = None,
        iot_groups_ids: Optional[str] = None,
        categories: Optional[str] = None,
        vendors: Optional[str] = None,
        models: Optional[str] = None,
        locations: Optional[str] = None,
        internal_ips: Optional[str] = None,
        mac_addresses: Optional[str] = None,
        first_seen_start: Optional[str] = None,
        first_seen_end: Optional[str] = None,
        last_seen_start: Optional[str] = None,
        last_seen_end: Optional[str] = None,
        show_expired: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Trigger a rescan of IoT device details for devices matching the filter.

        Forces FortiEDR to re-probe and update the fingerprinting information
        for the selected IoT devices.

        Args:
            organization: Organization name or None for all.
            devices: Comma-separated device names.
            devices_ids: Comma-separated device IDs.
            iot_groups: Comma-separated IoT group names.
            iot_groups_ids: Comma-separated IoT group IDs.
            categories: Comma-separated device categories.
            vendors: Comma-separated vendor names.
            models: Comma-separated model names.
            locations: Comma-separated location names.
            internal_ips: Comma-separated internal IP addresses.
            mac_addresses: Comma-separated MAC addresses.
            first_seen_start: ISO-8601 first-seen start filter.
            first_seen_end: ISO-8601 first-seen end filter.
            last_seen_start: ISO-8601 last-seen start filter.
            last_seen_end: ISO-8601 last-seen end filter.
            show_expired: Include expired records.
            strict_mode: Use exact matching.
            items_per_page: Results per page.
            page_number: Page number.
            sorting: Sort expression.
        """
        return await client.put(
            "/management-rest/iot/rescan-iot-device-details",
            params=_iot_filter(
                organization=organization, devices=devices,
                devices_ids=devices_ids, iot_groups=iot_groups,
                iot_groups_ids=iot_groups_ids, categories=categories,
                vendors=vendors, models=models, locations=locations,
                internal_ips=internal_ips, mac_addresses=mac_addresses,
                first_seen_start=first_seen_start,
                first_seen_end=first_seen_end,
                last_seen_start=last_seen_start, last_seen_end=last_seen_end,
                show_expired=show_expired, strict_mode=strict_mode,
                items_per_page=items_per_page, page_number=page_number,
                sorting=sorting,
            ),
        )

    @mcp.tool()
    async def iot_delete_devices(
        organization: Optional[str] = None,
        devices: Optional[str] = None,
        devices_ids: Optional[str] = None,
        iot_groups: Optional[str] = None,
        iot_groups_ids: Optional[str] = None,
        categories: Optional[str] = None,
        vendors: Optional[str] = None,
        models: Optional[str] = None,
        locations: Optional[str] = None,
        internal_ips: Optional[str] = None,
        mac_addresses: Optional[str] = None,
        first_seen_start: Optional[str] = None,
        first_seen_end: Optional[str] = None,
        last_seen_start: Optional[str] = None,
        last_seen_end: Optional[str] = None,
        show_expired: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Delete IoT device records matching the filter criteria.

        WARNING: This removes device records permanently from FortiEDR.

        Args:
            organization: Organization name or None for all.
            devices: Comma-separated device names to delete.
            devices_ids: Comma-separated device IDs to delete.
            iot_groups: Comma-separated IoT group names.
            iot_groups_ids: Comma-separated IoT group IDs.
            categories: Filter by device category.
            vendors: Filter by vendor name.
            models: Filter by model name.
            locations: Filter by location.
            internal_ips: Filter by internal IP address.
            mac_addresses: Filter by MAC address.
            first_seen_start: ISO-8601 first-seen start filter.
            first_seen_end: ISO-8601 first-seen end filter.
            last_seen_start: ISO-8601 last-seen start filter.
            last_seen_end: ISO-8601 last-seen end filter.
            show_expired: Include expired records.
            strict_mode: Use exact matching.
            items_per_page: Results per page.
            page_number: Page number.
            sorting: Sort expression.
        """
        return await client.delete(
            "/management-rest/iot/delete-devices",
            params=_iot_filter(
                organization=organization, devices=devices,
                devices_ids=devices_ids, iot_groups=iot_groups,
                iot_groups_ids=iot_groups_ids, categories=categories,
                vendors=vendors, models=models, locations=locations,
                internal_ips=internal_ips, mac_addresses=mac_addresses,
                first_seen_start=first_seen_start,
                first_seen_end=first_seen_end,
                last_seen_start=last_seen_start, last_seen_end=last_seen_end,
                show_expired=show_expired, strict_mode=strict_mode,
                items_per_page=items_per_page, page_number=page_number,
                sorting=sorting,
            ),
        )
