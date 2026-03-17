"""Exceptions tools – create, list and delete FortiEDR detection exceptions."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all exceptions tools on the given FastMCP instance."""

    @mcp.tool()
    async def exceptions_list_exceptions(
        organization: Optional[str] = None,
        exception_ids: Optional[str] = None,
        process: Optional[str] = None,
        path: Optional[str] = None,
        destination: Optional[str] = None,
        rules: Optional[str] = None,
        user: Optional[str] = None,
        collector_groups: Optional[str] = None,
        comment: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        updated_after: Optional[str] = None,
        updated_before: Optional[str] = None,
    ) -> Any:
        """List FortiEDR detection exceptions with optional filtering.

        Returns all configured exceptions that suppress alerts for known
        benign behavior patterns.

        Args:
            organization: Organization name or None for all.
            exception_ids: Comma-separated exception IDs to retrieve.
            process: Filter by process name in the exception.
            path: Filter by file path in the exception.
            destination: Filter by destination IP/hostname.
            rules: Comma-separated rule names the exception applies to.
            user: Filter by username the exception applies to.
            collector_groups: Comma-separated collector group names.
            comment: Filter by comment text (partial match).
            created_after: ISO-8601 datetime – show exceptions created after.
            created_before: ISO-8601 datetime – show exceptions created before.
            updated_after: ISO-8601 datetime – show exceptions updated after.
            updated_before: ISO-8601 datetime – show exceptions updated before.
        """
        return await client.get(
            "/management-rest/exceptions/list-exceptions",
            params={
                "organization": organization,
                "exceptionIds": exception_ids,
                "process": process,
                "path": path,
                "destination": destination,
                "rules": rules,
                "user": user,
                "collectorGroups": collector_groups,
                "comment": comment,
                "createdAfter": created_after,
                "createdBefore": created_before,
                "updatedAfter": updated_after,
                "updatedBefore": updated_before,
            },
        )

    @mcp.tool()
    async def exceptions_get_event_exceptions(
        event_id: int,
        organization: Optional[str] = None,
    ) -> Any:
        """List all exceptions associated with a specific security event.

        Args:
            event_id: The event ID to retrieve exceptions for.
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/exceptions/get-event-exceptions",
            params={
                "eventId": event_id,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def exceptions_create_or_edit_exception(
        organization: Optional[str] = None,
        confirm_edit: Optional[bool] = None,
        # Body – exception definition (pass as JSON-serializable dict string)
        exception_definition: Optional[dict] = None,
    ) -> Any:
        """Create a new FortiEDR exception or update an existing one.

        Accepts a full exception definition as a dictionary. The structure
        matches the FortiEDR exception schema (process, path, destination,
        rules, collector groups, users, etc.).

        Args:
            organization: Organization name or None for all.
            confirm_edit: Set to True to confirm editing an existing exception
                that would affect multiple events.
            exception_definition: Dictionary containing the exception fields
                (process, path, destination, rules, collectorGroups, users,
                comment, etc.).
        """
        return await client.post(
            "/management-rest/exceptions/create-or-edit-exception",
            params={
                "organization": organization,
                "confirmEdit": confirm_edit,
            },
            json=exception_definition or {},
        )

    @mcp.tool()
    async def exceptions_delete(
        organization: Optional[str] = None,
        exception_id: Optional[int] = None,
        exception_ids: Optional[str] = None,
        process: Optional[str] = None,
        path: Optional[str] = None,
        destination: Optional[str] = None,
        rules: Optional[str] = None,
        user: Optional[str] = None,
        collector_groups: Optional[str] = None,
        comment: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        updated_after: Optional[str] = None,
        updated_before: Optional[str] = None,
        delete_all: Optional[bool] = None,
    ) -> Any:
        """Delete FortiEDR exceptions matching the given criteria.

        WARNING: Deletion is permanent. Use filters carefully.

        Args:
            organization: Organization name or None for all.
            exception_id: Single exception ID to delete.
            exception_ids: Comma-separated exception IDs to delete.
            process: Delete exceptions matching this process name.
            path: Delete exceptions matching this file path.
            destination: Delete exceptions matching this destination.
            rules: Comma-separated rule names to filter deletions.
            user: Delete exceptions for this username.
            collector_groups: Comma-separated collector group names.
            comment: Delete exceptions with matching comment.
            created_after: Delete exceptions created after this ISO-8601 datetime.
            created_before: Delete exceptions created before this ISO-8601 datetime.
            updated_after: Delete exceptions updated after this ISO-8601 datetime.
            updated_before: Delete exceptions updated before this ISO-8601 datetime.
            delete_all: If True, deletes all exceptions matching the filter.
        """
        return await client.delete(
            "/management-rest/exceptions/delete",
            params={
                "organization": organization,
                "exceptionId": exception_id,
                "exceptionIds": exception_ids,
                "process": process,
                "path": path,
                "destination": destination,
                "rules": rules,
                "user": user,
                "collectorGroups": collector_groups,
                "comment": comment,
                "createdAfter": created_after,
                "createdBefore": created_before,
                "updatedAfter": updated_after,
                "updatedBefore": updated_before,
                "deleteAll": delete_all,
            },
        )
