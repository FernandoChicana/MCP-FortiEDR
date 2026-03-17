"""Playbooks Policies tools – manage automated response playbook policies."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all playbooks-policies tools on the given FastMCP instance."""

    @mcp.tool()
    async def playbooks_list_policies(
        organization: Optional[str] = None,
    ) -> Any:
        """List all automated response playbook policies.

        Returns FortiEDR playbook policies that define automated response
        actions triggered by security events.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/playbooks-policies/list-policies",
            params={"organization": organization},
        )

    @mcp.tool()
    async def playbooks_clone_policy(
        source_policy_name: str,
        new_policy_name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Clone an existing playbook policy under a new name.

        Args:
            source_policy_name: Name of the policy to clone.
            new_policy_name: Name for the new cloned policy.
            organization: Organization name or None for all.
        """
        return await client.post(
            "/management-rest/playbooks-policies/clone",
            params={
                "sourcePolicyName": source_policy_name,
                "newPolicyName": new_policy_name,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def playbooks_assign_collector_group(
        policy_name: str,
        collector_group_names: str,
        organization: Optional[str] = None,
        force_assign: Optional[bool] = None,
    ) -> Any:
        """Assign collector groups to a playbook policy.

        Args:
            policy_name: Name of the playbook policy.
            collector_group_names: Comma-separated collector group names.
            organization: Organization name or None for all.
            force_assign: Force assignment even if conflicts exist.
        """
        return await client.put(
            "/management-rest/playbooks-policies/assign-collector-group",
            params={
                "policyName": policy_name,
                "collectorGroupNames": collector_group_names,
                "organization": organization,
                "forceAssign": force_assign,
            },
        )

    @mcp.tool()
    async def playbooks_set_mode(
        policy_name: str,
        mode: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Set the operating mode of a playbook policy.

        Args:
            policy_name: Name of the playbook policy to change.
            mode: Target mode: 'Simulation' or 'Prevention'.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/playbooks-policies/set-mode",
            params={
                "policyName": policy_name,
                "mode": mode,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def playbooks_map_connectors_to_actions(
        policy_name: str,
        organization: Optional[str] = None,
        fortinet_actions_to_connectors_maps: Optional[str] = None,
        custom_actions_to_connectors_maps: Optional[str] = None,
    ) -> Any:
        """Map external connectors to playbook action triggers.

        Associates SIEM/SOAR/ticketing connectors with specific playbook
        actions so that automated responses use the correct integration.

        Args:
            policy_name: Name of the playbook policy to configure.
            organization: Organization name or None for all.
            fortinet_actions_to_connectors_maps: JSON mapping of Fortinet
                built-in action names to connector names.
            custom_actions_to_connectors_maps: JSON mapping of custom
                action names to connector names.
        """
        return await client.put(
            "/management-rest/playbooks-policies/map-connectors-to-actions",
            params={"organization": organization},
            json={
                "policyName": policy_name,
                "fortinetActionsToConnectorsMaps": fortinet_actions_to_connectors_maps,
                "customActionsToConnectorsMaps": custom_actions_to_connectors_maps,
            },
        )

    @mcp.tool()
    async def playbooks_set_action_classification(
        policy_name: str,
        organization: Optional[str] = None,
        fortinet_actions_to_classification_maps: Optional[str] = None,
        custom_actions_to_classification_maps: Optional[str] = None,
    ) -> Any:
        """Set event classification mappings for playbook actions.

        Defines which event classifications trigger specific playbook actions
        within a policy.

        Args:
            policy_name: Name of the playbook policy to configure.
            organization: Organization name or None for all.
            fortinet_actions_to_classification_maps: JSON mapping of Fortinet
                action names to event classifications.
            custom_actions_to_classification_maps: JSON mapping of custom
                action names to event classifications.
        """
        return await client.put(
            "/management-rest/playbooks-policies/set-action-classification",
            params={"organization": organization},
            json={
                "policyName": policy_name,
                "fortinetActionsToClassificationMaps": fortinet_actions_to_classification_maps,
                "customActionsToClassificationMaps": custom_actions_to_classification_maps,
            },
        )
