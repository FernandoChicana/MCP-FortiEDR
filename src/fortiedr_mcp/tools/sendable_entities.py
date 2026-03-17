"""Sendable Entities tools – configure email notification formats."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all sendable-entities tools on the given FastMCP instance."""

    @mcp.tool()
    async def sendable_entities_set_mail_format(
        format: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Set the email notification format for FortiEDR alert emails.

        Configures whether alert notification emails are sent in plain text
        or HTML format.

        Args:
            format: Email format: 'Text' for plain text or 'Html' for HTML.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/sendable-entities/set-mail-format",
            params={"format": format, "organization": organization},
        )
