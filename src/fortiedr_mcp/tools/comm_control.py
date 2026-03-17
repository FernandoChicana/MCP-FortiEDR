"""Communication Control tools – manage application communication policies."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all communication-control tools on the given FastMCP instance."""

    @mcp.tool()
    async def comm_control_assign_collector_group(
        policy_name: str,
        collector_groups: str,
        organization: Optional[str] = None,
        force_assign: Optional[bool] = None,
    ) -> Any:
        """Assign one or more collector groups to an application communication policy.

        Args:
            policy_name: Name of the communication control policy to assign groups to.
            collector_groups: Comma-separated list of collector group names to assign.
            organization: Organization name or None for all organizations.
            force_assign: If True, forces assignment even if the group is already
                assigned to another policy.
        """
        return await client.put(
            "/management-rest/comm-control/assign-collector-group",
            params={
                "policyName": policy_name,
                "collectorGroups": collector_groups,
                "organization": organization,
                "forceAssign": force_assign,
            },
        )

    @mcp.tool()
    async def comm_control_clone_policy(
        source_policy_name: str,
        new_policy_name: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Clone an existing communication control policy under a new name.

        Args:
            source_policy_name: Name of the policy to clone.
            new_policy_name: Name for the new cloned policy.
            organization: Organization name or None for all organizations.
        """
        return await client.post(
            "/management-rest/comm-control/clone-policy",
            params={
                "sourcePolicyName": source_policy_name,
                "newPolicyName": new_policy_name,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def comm_control_list_policies(
        organization: Optional[str] = None,
        policies: Optional[str] = None,
        rules: Optional[str] = None,
        sources: Optional[str] = None,
        decisions: Optional[str] = None,
        state: Optional[str] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """List communication control policies with optional filtering.

        Returns the set of application communication policies, including their
        rules, assigned collector groups, and current modes.

        Args:
            organization: Organization name or None for all.
            policies: Comma-separated list of specific policy names to retrieve.
            rules: Comma-separated rule names to filter by.
            sources: Comma-separated source names/IPs to filter by.
            decisions: Comma-separated decision values (Allow, Block, etc.).
            state: Filter by policy state (e.g., 'Enabled', 'Disabled').
            strict_mode: If True, use exact match for string filters.
            items_per_page: Number of results per page (pagination).
            page_number: Page number to retrieve (1-based, pagination).
            sorting: Sort field and direction, e.g. 'name asc'.
        """
        return await client.get(
            "/management-rest/comm-control/list-policies",
            params={
                "organization": organization,
                "policies": policies,
                "rules": rules,
                "sources": sources,
                "decisions": decisions,
                "state": state,
                "strictMode": strict_mode,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def comm_control_list_products(
        organization: Optional[str] = None,
        product: Optional[str] = None,
        products: Optional[str] = None,
        vendor: Optional[str] = None,
        vendors: Optional[str] = None,
        version: Optional[str] = None,
        versions: Optional[str] = None,
        os: Optional[str] = None,
        action: Optional[str] = None,
        reputation: Optional[str] = None,
        handled: Optional[bool] = None,
        seen: Optional[bool] = None,
        policies: Optional[str] = None,
        rule: Optional[str] = None,
        rule_policy: Optional[str] = None,
        devices: Optional[str] = None,
        ips: Optional[str] = None,
        destination_ip: Optional[str] = None,
        collector_groups: Optional[str] = None,
        process_hash: Optional[str] = None,
        processes: Optional[str] = None,
        cve_identifier: Optional[str] = None,
        vulnerabilities: Optional[str] = None,
        include_statistics: Optional[bool] = None,
        first_connection_time_start: Optional[str] = None,
        first_connection_time_end: Optional[str] = None,
        last_connection_time_start: Optional[str] = None,
        last_connection_time_end: Optional[str] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """List applications communicating through FortiEDR-monitored endpoints.

        Returns a paginated list of network communicating applications with
        associated reputation, policy decisions, and connection metadata.

        Args:
            organization: Organization name or None for all.
            product: Single product name to filter.
            products: Comma-separated product names to filter.
            vendor: Single vendor name to filter.
            vendors: Comma-separated vendor names.
            version: Single version string to filter.
            versions: Comma-separated version strings.
            os: OS filter (e.g., 'Windows', 'Linux').
            action: Filter by action taken (e.g., 'Allow', 'Block').
            reputation: Filter by reputation score/label.
            handled: If True, show only handled applications.
            seen: If True, show only seen applications.
            policies: Comma-separated policy names to filter by.
            rule: Single rule name filter.
            rule_policy: Policy name for rule filter.
            devices: Comma-separated device names.
            ips: Comma-separated device IP addresses.
            destination_ip: Filter by destination IP address.
            collector_groups: Comma-separated collector group names.
            process_hash: File hash of the communicating process.
            processes: Comma-separated process names.
            cve_identifier: CVE ID to filter by vulnerability.
            vulnerabilities: Comma-separated vulnerability names.
            include_statistics: If True, include connection statistics.
            first_connection_time_start: ISO-8601 start for first-seen filter.
            first_connection_time_end: ISO-8601 end for first-seen filter.
            last_connection_time_start: ISO-8601 start for last-seen filter.
            last_connection_time_end: ISO-8601 end for last-seen filter.
            strict_mode: If True, use exact match for string filters.
            items_per_page: Results per page (pagination).
            page_number: Page number (1-based).
            sorting: Sort field and direction.
        """
        return await client.get(
            "/management-rest/comm-control/list-products",
            params={
                "organization": organization,
                "product": product,
                "products": products,
                "vendor": vendor,
                "vendors": vendors,
                "version": version,
                "versions": versions,
                "os": os,
                "action": action,
                "reputation": reputation,
                "handled": handled,
                "seen": seen,
                "policies": policies,
                "rule": rule,
                "rulePolicy": rule_policy,
                "devices": devices,
                "ips": ips,
                "destinationIp": destination_ip,
                "collectorGroups": collector_groups,
                "processHash": process_hash,
                "processes": processes,
                "cveIdentifier": cve_identifier,
                "vulnerabilities": vulnerabilities,
                "includeStatistics": include_statistics,
                "firstConnectionTimeStart": first_connection_time_start,
                "firstConnectionTimeEnd": first_connection_time_end,
                "lastConnectionTimeStart": last_connection_time_start,
                "lastConnectionTimeEnd": last_connection_time_end,
                "strictMode": strict_mode,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def comm_control_resolve_applications(
        organization: Optional[str] = None,
        products: Optional[str] = None,
        vendors: Optional[str] = None,
        versions: Optional[str] = None,
        resolve: Optional[bool] = None,
        signed: Optional[bool] = None,
        apply_nested: Optional[bool] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Mark communicating applications as resolved or unresolved.

        Args:
            organization: Organization name or None for all.
            products: Comma-separated product names to resolve/unresolve.
            vendors: Comma-separated vendor names.
            versions: Comma-separated version strings.
            resolve: True to mark as resolved, False to unresolve.
            signed: Filter to only signed (True) or unsigned (False) apps.
            apply_nested: If True, apply recursively to nested versions.
            comment: Optional comment explaining the resolution action.
        """
        return await client.put(
            "/management-rest/comm-control/resolve-applications",
            params={
                "organization": organization,
                "products": products,
                "vendors": vendors,
                "versions": versions,
                "resolve": resolve,
                "signed": signed,
                "applyNested": apply_nested,
                "comment": comment,
            },
        )

    @mcp.tool()
    async def comm_control_set_policy_mode(
        policy_names: str,
        mode: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Set one or more communication control policies to Simulation or Prevention mode.

        Args:
            policy_names: Comma-separated list of policy names to change.
            mode: Target mode: 'Simulation' or 'Prevention'.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/comm-control/set-policy-mode",
            params={
                "policyNames": policy_names,
                "mode": mode,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def comm_control_set_policy_permission(
        policies: str,
        decision: str,
        organization: Optional[str] = None,
        products: Optional[str] = None,
        vendors: Optional[str] = None,
        versions: Optional[str] = None,
        signed: Optional[bool] = None,
        apply_nested: Optional[bool] = None,
    ) -> Any:
        """Set Allow or Deny permission for applications in a communication policy.

        Args:
            policies: Comma-separated policy names to modify.
            decision: Permission decision: 'Allow' or 'Deny'.
            organization: Organization name or None for all.
            products: Comma-separated product names to apply the decision to.
            vendors: Comma-separated vendor names.
            versions: Comma-separated version strings.
            signed: Filter to only signed (True) or unsigned (False) apps.
            apply_nested: If True, apply recursively to nested items.
        """
        return await client.put(
            "/management-rest/comm-control/set-policy-permission",
            params={
                "policies": policies,
                "decision": decision,
                "organization": organization,
                "products": products,
                "vendors": vendors,
                "versions": versions,
                "signed": signed,
                "applyNested": apply_nested,
            },
        )

    @mcp.tool()
    async def comm_control_set_policy_rule_state(
        policy_name: str,
        rule_name: str,
        state: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Enable or disable a specific rule within a communication control policy.

        Args:
            policy_name: Name of the policy containing the rule.
            rule_name: Name of the rule to change.
            state: 'Enabled' or 'Disabled'.
            organization: Organization name or None for all.
        """
        return await client.put(
            "/management-rest/comm-control/set-policy-rule-state",
            params={
                "policyName": policy_name,
                "ruleName": rule_name,
                "state": state,
                "organization": organization,
            },
        )
