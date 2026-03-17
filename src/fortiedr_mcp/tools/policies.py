"""Policies tools – manage FortiEDR security detection policies."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all policies tools on the given FastMCP instance."""

    @mcp.tool()
    async def policies_list(
        organization: Optional[str] = None,
    ) -> Any:
        """List all FortiEDR security detection policies.

        Returns the detection policies with their rules, modes, and
        collector group assignments.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/policies/list-policies",
            params={"organization": organization},
        )

    @mcp.tool()
    async def policies_clone(
        source_policy_name: str,
        new_policy_name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Clone a security detection policy under a new name.

        Args:
            source_policy_name: Name of the policy to clone.
            new_policy_name: Name for the new cloned policy.
            organization: Organization name or None for all.
        """
        return await client.post(
            "/management-rest/policies/clone",
            params={
                "sourcePolicyName": source_policy_name,
                "newPolicyName": new_policy_name,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def policies_assign_collector_group(
        policy_name: str,
        collectors_group_name: str,
        organization: Optional[str] = None,
        force_assign: Optional[bool] = None,
    ) -> Any:
        """Assign a collector group to a security detection policy.

        Args:
            policy_name: Name of the detection policy.
            collectors_group_name: Name of the collector group to assign.
            organization: Organization name or None for all.
            force_assign: If True, force assignment even if conflicts exist.
        """
        return await client.put(
            "/management-rest/policies/assign-collector-group",
            params={
                "policyName": policy_name,
                "collectorsGroupName": collectors_group_name,
                "organization": organization,
                "forceAssign": force_assign,
            },
        )

    @mcp.tool()
    async def policies_set_mode(
        policy_name: str,
        mode: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Set a security detection policy to Simulation or Prevention mode.

        Args:
            policy_name: Name of the policy to change.
            mode: Target mode: 'Simulation' or 'Prevention'.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/policies/set-mode",
            params={
                "policyName": policy_name,
                "mode": mode,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def policies_set_rule_state(
        policy_name: str,
        rule_name: str,
        state: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Enable or disable a detection rule within a security policy.

        Args:
            policy_name: Name of the policy containing the rule.
            rule_name: Name of the detection rule to change.
            state: 'Enabled' to activate the rule, 'Disabled' to deactivate.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/policies/set-policy-rule-state",
            params={
                "policyName": policy_name,
                "ruleName": rule_name,
                "state": state,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def policies_set_rule_action(
        policy_name: str,
        rule_name: str,
        action: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Set the action taken when a detection rule fires in a policy.

        Args:
            policy_name: Name of the policy containing the rule.
            rule_name: Name of the detection rule.
            action: Action to take on rule trigger (e.g., 'Block', 'Simulate',
                'Log').
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/policies/set-policy-rule-action",
            params={
                "policyName": policy_name,
                "ruleName": rule_name,
                "action": action,
                "organization": organization,
            },
        )
