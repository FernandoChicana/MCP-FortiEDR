"""Users tools – manage FortiEDR user accounts and authentication settings."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all users tools on the given FastMCP instance."""

    @mcp.tool()
    async def users_list(
        organization: Optional[str] = None,
    ) -> Any:
        """List all user accounts in FortiEDR.

        Returns users with their roles, email addresses, and assigned
        organizations.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/users/list-users",
            params={"organization": organization},
        )

    @mcp.tool()
    async def users_create(
        username: str,
        password: str,
        confirm_password: str,
        email: str,
        roles: str,
        organization: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Any:
        """Create a new FortiEDR user account.

        Args:
            username: Unique login username.
            password: Initial password for the account.
            confirm_password: Must match password.
            email: Email address for notifications and password recovery.
            roles: Comma-separated role names to assign
                (e.g., 'Admin', 'SOC Operator', 'Read Only').
            organization: Organization to create the user in.
            first_name: User's first name.
            last_name: User's last name.
            title: User's job title.
        """
        return await client.post(
            "/management-rest/users/create-user",
            params={"organization": organization},
            json={
                "username": username,
                "password": password,
                "confirmPassword": confirm_password,
                "email": email,
                "roles": roles,
                "firstName": first_name,
                "lastName": last_name,
                "title": title,
            },
        )

    @mcp.tool()
    async def users_update(
        username: str,
        organization: Optional[str] = None,
        new_username: Optional[str] = None,
        email: Optional[str] = None,
        roles: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Any:
        """Update an existing FortiEDR user account.

        Args:
            username: Username of the account to update.
            organization: Organization name or None for all.
            new_username: New username (if changing the login name).
            email: New email address.
            roles: New comma-separated role assignments.
            first_name: Updated first name.
            last_name: Updated last name.
            title: Updated job title.
        """
        return await client.put(
            "/management-rest/users/update-user",
            params={"username": username, "organization": organization},
            json={
                "username": new_username,
                "email": email,
                "roles": roles,
                "firstName": first_name,
                "lastName": last_name,
                "title": title,
            },
        )

    @mcp.tool()
    async def users_delete(
        username: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Delete a FortiEDR user account.

        Args:
            username: Username of the account to delete.
            organization: Organization name or None for all.
        """
        return await client.delete(
            "/management-rest/users/delete-user",
            params={"username": username, "organization": organization},
        )

    @mcp.tool()
    async def users_reset_password(
        username: str,
        password: str,
        confirm_password: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Reset a FortiEDR user's password.

        Args:
            username: Username of the account to reset.
            password: New password.
            confirm_password: Must match the new password.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/users/reset-password",
            params={"username": username, "organization": organization},
            json={
                "password": password,
                "confirmPassword": confirm_password,
            },
        )

    @mcp.tool()
    async def users_get_sp_metadata(
        organization: Optional[str] = None,
    ) -> Any:
        """Get SAML Service Provider metadata for SSO configuration.

        Returns the XML metadata needed to configure FortiEDR as a Service
        Provider in an Identity Provider (IdP) like Azure AD or Okta.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/users/get-sp-metadata",
            params={"organization": organization},
        )

    @mcp.tool()
    async def users_delete_saml_settings(
        organization_name_request: Optional[str] = None,
    ) -> Any:
        """Delete SAML/SSO settings for an organization.

        Removes the SAML Identity Provider configuration, reverting
        authentication to local user accounts.

        Args:
            organization_name_request: Name of the organization whose
                SAML settings to delete.
        """
        return await client.delete(
            "/management-rest/users/delete-saml-settings",
            params={"organizationNameRequest": organization_name_request},
        )
