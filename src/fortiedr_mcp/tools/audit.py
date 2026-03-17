"""Audit tools – retrieve audit log entries."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all audit tools on the given FastMCP instance."""

    @mcp.tool()
    async def audit_get_audit(
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Retrieve FortiEDR audit log entries within a date range.

        Returns a list of audit events recording administrative and security
        actions performed by users or the system.

        Args:
            from_time: Start of the time range in ISO-8601 format,
                e.g. '2024-01-01T00:00:00'.
            to_time: End of the time range in ISO-8601 format,
                e.g. '2024-01-31T23:59:59'.
            organization: Organization name or None for all organizations.
        """
        return await client.get(
            "/management-rest/audit/get-audit",
            params={
                "fromTime": from_time,
                "toTime": to_time,
                "organization": organization,
            },
        )
