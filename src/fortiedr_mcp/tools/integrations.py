"""Integrations tools – manage FortiEDR external connectors (SIEM, SOAR, ticketing)."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all integrations tools on the given FastMCP instance."""

    @mcp.tool()
    async def integrations_list_connectors(
        organization: Optional[str] = None,
        only_valid_connectors: Optional[bool] = None,
    ) -> Any:
        """List all external connectors configured in FortiEDR.

        Returns SIEM, SOAR, ticketing, and other integration connectors
        with their type, host, status, and configured actions.

        Args:
            organization: Organization name or None for all.
            only_valid_connectors: If True, return only connectors with
                a valid (reachable) connection status.
        """
        return await client.get(
            "/management-rest/integrations/list-connectors",
            params={
                "organization": organization,
                "onlyValidConnectors": only_valid_connectors,
            },
        )

    @mcp.tool()
    async def integrations_connectors_metadata(
        organization: Optional[str] = None,
    ) -> Any:
        """Get metadata describing available connector types and their valid field values.

        Returns the schema of supported connector types, required fields,
        and allowed values to use when creating or updating connectors.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/integrations/connectors-metadata",
            params={"organization": organization},
        )

    @mcp.tool()
    async def integrations_create_connector(
        name: str,
        type: str,
        vendor: str,
        host: str,
        organization: Optional[str] = None,
        port: Optional[str] = None,
        enabled: Optional[bool] = None,
        connector_actions: Optional[str] = None,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        core_id: Optional[int] = None,
    ) -> Any:
        """Create a new external connector in FortiEDR.

        Registers a new SIEM, SOAR, or ticketing integration connector so
        FortiEDR can forward events and trigger automated actions.

        Args:
            name: Display name for the connector.
            type: Connector type identifier (e.g., 'Syslog', 'ServiceNow').
            vendor: Vendor name for the connector.
            host: Hostname or IP address of the connector target.
            organization: Organization to create the connector for.
            port: TCP port for the connector (as string).
            enabled: If True, the connector is active immediately.
            connector_actions: JSON string of actions to configure.
            api_key: API key for authentication (if applicable).
            username: Username for authentication (if applicable).
            password: Password for authentication (if applicable).
            core_id: FortiEDR core ID to route through (if applicable).
        """
        return await client.post(
            "/management-rest/integrations/create-connector",
            json={
                "name": name,
                "type": type,
                "vendor": vendor,
                "host": host,
                "organization": organization,
                "port": port,
                "enabled": enabled,
                "connectorActions": connector_actions,
                "apiKey": api_key,
                "username": username,
                "password": password,
                "coreId": core_id,
            },
        )

    @mcp.tool()
    async def integrations_update_connector(
        name: str,
        type: str,
        vendor: str,
        host: str,
        organization: Optional[str] = None,
        port: Optional[str] = None,
        enabled: Optional[bool] = None,
        connector_actions: Optional[str] = None,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        core_id: Optional[int] = None,
    ) -> Any:
        """Update an existing external connector in FortiEDR.

        Args:
            name: Name of the connector to update (must match existing name).
            type: Connector type identifier.
            vendor: Vendor name.
            host: New hostname or IP address.
            organization: Organization name.
            port: New TCP port (as string).
            enabled: Enable or disable the connector.
            connector_actions: Updated JSON string of actions.
            api_key: New API key.
            username: New username.
            password: New password.
            core_id: New core ID routing.
        """
        return await client.put(
            "/management-rest/integrations/update-connector",
            json={
                "name": name,
                "type": type,
                "vendor": vendor,
                "host": host,
                "organization": organization,
                "port": port,
                "enabled": enabled,
                "connectorActions": connector_actions,
                "apiKey": api_key,
                "username": username,
                "password": password,
                "coreId": core_id,
            },
        )

    @mcp.tool()
    async def integrations_delete_connector(
        connector_name: str,
        connector_type: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Delete an external connector from FortiEDR.

        Args:
            connector_name: Name of the connector to delete.
            connector_type: Type of the connector to delete.
            organization: Organization name or None for all.
        """
        return await client.delete(
            "/management-rest/integrations/delete-connector",
            params={
                "connectorName": connector_name,
                "connectorType": connector_type,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def integrations_test_connector(
        connector_name: str,
        connector_type: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Test connectivity to an external connector.

        Sends a test message to verify that FortiEDR can reach and authenticate
        with the specified external connector.

        Args:
            connector_name: Name of the connector to test.
            connector_type: Type of the connector.
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/integrations/test-connector",
            params={
                "connectorName": connector_name,
                "connectorType": connector_type,
                "organization": organization,
            },
        )
