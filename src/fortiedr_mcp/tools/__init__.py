"""Tool registration for all FortiEDR MCP tools.

Each sub-module corresponds to one API category from the FortiEDR REST API.
"""

from fastmcp import FastMCP

from . import (
    admin,
    audit,
    comm_control,
    events,
    exceptions,
    forensics,
    hash,
    integrations,
    inventory,
    iot,
    ip_sets,
    organizations,
    playbooks_policies,
    policies,
    sendable_entities,
    system_events,
    threat_hunting,
    threat_hunting_exclusions,
    threat_hunting_settings,
    users,
)

_MODULES = [
    admin,
    audit,
    comm_control,
    events,
    exceptions,
    forensics,
    hash,
    integrations,
    inventory,
    iot,
    ip_sets,
    organizations,
    playbooks_policies,
    policies,
    sendable_entities,
    system_events,
    threat_hunting,
    threat_hunting_exclusions,
    threat_hunting_settings,
    users,
]


def register_all(mcp: FastMCP) -> None:
    """Register tools from all categories on the given FastMCP instance."""
    for module in _MODULES:
        module.register(mcp)
