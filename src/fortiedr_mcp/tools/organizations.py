"""Organizations tools – manage multi-tenant FortiEDR organizations."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all organizations tools on the given FastMCP instance."""

    @mcp.tool()
    async def organizations_list() -> Any:
        """List all organizations configured in this FortiEDR instance.

        Returns organization names, license details, and feature flags.
        """
        return await client.get("/management-rest/organizations/list-organizations")

    @mcp.tool()
    async def organizations_create(
        name: str,
        password: str,
        password_confirmation: str,
        expiration_date: Optional[str] = None,
        workstations_allocated: Optional[int] = None,
        servers_allocated: Optional[int] = None,
        iot_allocated: Optional[int] = None,
        edr: Optional[bool] = None,
        edr_enabled: Optional[bool] = None,
        edr_storage_allocated_in_mb: Optional[int] = None,
        edr_add_ons_allocated: Optional[int] = None,
        edr_number_of_shards: Optional[int] = None,
        edr_backup_enabled: Optional[bool] = None,
        forensics: Optional[bool] = None,
        vulnerability_and_iot: Optional[bool] = None,
        extended_detection: Optional[bool] = None,
        request_policy_engine_lib_updates: Optional[bool] = None,
        serial_number: Optional[str] = None,
    ) -> Any:
        """Create a new organization in FortiEDR (multi-tenant setup).

        Args:
            name: Unique name for the new organization.
            password: Initial admin password for the organization.
            password_confirmation: Must match password.
            expiration_date: License expiration date (ISO-8601).
            workstations_allocated: Maximum workstation collector seats.
            servers_allocated: Maximum server collector seats.
            iot_allocated: Maximum IoT device seats.
            edr: Enable EDR module for this organization.
            edr_enabled: Activate the EDR module.
            edr_storage_allocated_in_mb: EDR storage quota in megabytes.
            edr_add_ons_allocated: EDR add-on seats.
            edr_number_of_shards: Number of data shards for EDR storage.
            edr_backup_enabled: Enable EDR data backup.
            forensics: Enable forensics module.
            vulnerability_and_iot: Enable vulnerability and IoT module.
            extended_detection: Enable extended detection features.
            request_policy_engine_lib_updates: Auto-request policy lib updates.
            serial_number: Hardware serial number for license binding.
        """
        return await client.post(
            "/management-rest/organizations/create-organization",
            json={
                "name": name,
                "password": password,
                "passwordConfirmation": password_confirmation,
                "expirationDate": expiration_date,
                "workstationsAllocated": workstations_allocated,
                "serversAllocated": servers_allocated,
                "iotAllocated": iot_allocated,
                "edr": edr,
                "edrEnabled": edr_enabled,
                "edrStorageAllocatedInMb": edr_storage_allocated_in_mb,
                "edrAddOnsAllocated": edr_add_ons_allocated,
                "edrNumberOfShards": edr_number_of_shards,
                "edrBackupEnabled": edr_backup_enabled,
                "forensics": forensics,
                "vulnerabilityAndIoT": vulnerability_and_iot,
                "eXtendedDetection": extended_detection,
                "requestPolicyEngineLibUpdates": request_policy_engine_lib_updates,
                "serialNumber": serial_number,
            },
        )

    @mcp.tool()
    async def organizations_update(
        organization: str,
        name: Optional[str] = None,
        expiration_date: Optional[str] = None,
        workstations_allocated: Optional[int] = None,
        servers_allocated: Optional[int] = None,
        iot_allocated: Optional[int] = None,
        edr: Optional[bool] = None,
        edr_enabled: Optional[bool] = None,
        edr_storage_allocated_in_mb: Optional[int] = None,
        edr_add_ons_allocated: Optional[int] = None,
        edr_number_of_shards: Optional[int] = None,
        edr_backup_enabled: Optional[bool] = None,
        forensics: Optional[bool] = None,
        vulnerability_and_iot: Optional[bool] = None,
        extended_detection: Optional[bool] = None,
        request_policy_engine_lib_updates: Optional[bool] = None,
        serial_number: Optional[str] = None,
    ) -> Any:
        """Update an existing organization's settings and license allocations.

        Args:
            organization: Current name of the organization to update.
            name: New name for the organization (rename).
            expiration_date: New expiration date (ISO-8601).
            workstations_allocated: New workstation seat count.
            servers_allocated: New server seat count.
            iot_allocated: New IoT device seat count.
            edr: Enable/disable EDR module.
            edr_enabled: Activate/deactivate EDR.
            edr_storage_allocated_in_mb: New EDR storage quota.
            edr_add_ons_allocated: New EDR add-on seats.
            edr_number_of_shards: New shard count for EDR storage.
            edr_backup_enabled: Enable/disable EDR backup.
            forensics: Enable/disable forensics module.
            vulnerability_and_iot: Enable/disable vulnerability and IoT.
            extended_detection: Enable/disable extended detection.
            request_policy_engine_lib_updates: Auto-update policy libs.
            serial_number: New hardware serial number.
        """
        return await client.put(
            "/management-rest/organizations/update-organization",
            params={"organization": organization},
            json={
                "name": name,
                "expirationDate": expiration_date,
                "workstationsAllocated": workstations_allocated,
                "serversAllocated": servers_allocated,
                "iotAllocated": iot_allocated,
                "edr": edr,
                "edrEnabled": edr_enabled,
                "edrStorageAllocatedInMb": edr_storage_allocated_in_mb,
                "edrAddOnsAllocated": edr_add_ons_allocated,
                "edrNumberOfShards": edr_number_of_shards,
                "edrBackupEnabled": edr_backup_enabled,
                "forensics": forensics,
                "vulnerabilityAndIoT": vulnerability_and_iot,
                "eXtendedDetection": extended_detection,
                "requestPolicyEngineLibUpdates": request_policy_engine_lib_updates,
                "serialNumber": serial_number,
            },
        )

    @mcp.tool()
    async def organizations_delete(
        organization: str,
    ) -> Any:
        """Delete an organization from FortiEDR.

        WARNING: This permanently removes the organization and all its data.

        Args:
            organization: Name of the organization to delete.
        """
        return await client.delete(
            "/management-rest/organizations/delete-organization",
            params={"organization": organization},
        )

    @mcp.tool()
    async def organizations_export(
        organization: str,
        destination_name: Optional[str] = None,
    ) -> Any:
        """Export an organization's configuration for backup or migration.

        Args:
            organization: Name of the organization to export.
            destination_name: Optional filename for the export archive.
        """
        return await client.get(
            "/management-rest/organizations/export-organization",
            params={
                "organization": organization,
                "destinationName": destination_name,
            },
        )

    @mcp.tool()
    async def organizations_transfer_collectors(
        source_organization: str,
        target_organization: str,
        verification_code: str,
        aggregators_map: Optional[str] = None,
    ) -> Any:
        """Transfer collector agents from one organization to another.

        Args:
            source_organization: Name of the source organization.
            target_organization: Name of the destination organization.
            verification_code: Security verification code for the transfer.
            aggregators_map: JSON mapping of source aggregators to target
                aggregators (if aggregator reassignment is needed).
        """
        return await client.post(
            "/management-rest/organizations/transfer-collectors",
            json={
                "sourceOrganization": source_organization,
                "targetOrganization": target_organization,
                "verificationCode": verification_code,
                "aggregatorsMap": aggregators_map,
            },
        )

    @mcp.tool()
    async def organizations_transfer_collectors_stop(
        organization: str,
    ) -> Any:
        """Stop an in-progress collector transfer operation.

        Args:
            organization: Organization name for which to stop the transfer.
        """
        return await client.post(
            "/management-rest/organizations/transfer-collectors-stop",
            params={"organization": organization},
        )
