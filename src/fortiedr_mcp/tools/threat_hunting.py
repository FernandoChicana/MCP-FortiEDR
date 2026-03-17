"""Threat Hunting tools – search, query, and analyze threat-hunting telemetry."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all threat-hunting tools on the given FastMCP instance."""

    @mcp.tool()
    async def threat_hunting_search(
        organization: Optional[str] = None,
        query: Optional[str] = None,
        category: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        time: Optional[str] = None,
        devices: Optional[str] = None,
        filters: Optional[str] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Search the FortiEDR threat-hunting telemetry repository.

        Executes a query against collected endpoint telemetry data for
        threat hunting and investigation. Supports FortiEDR query language
        for complex searches.

        Args:
            organization: Organization name or None for all.
            query: FortiEDR query language expression to filter results.
                Example: 'Process.Name = "powershell.exe"'.
            category: Telemetry category to search within
                (e.g., 'Process', 'Network', 'File', 'Registry').
            from_time: ISO-8601 start of the time range to search.
            to_time: ISO-8601 end of the time range to search.
            time: Relative time shorthand (e.g., '1h', '24h', '7d').
            devices: Comma-separated device names to search on.
            filters: JSON string of additional field filters.
            items_per_page: Results per page.
            page_number: Page number (1-based).
            sorting: Sort expression (e.g., 'time desc').
        """
        return await client.post(
            "/management-rest/threat-hunting/search",
            json={
                "organization": organization,
                "query": query,
                "category": category,
                "fromTime": from_time,
                "toTime": to_time,
                "time": time,
                "devices": devices,
                "filters": filters,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def threat_hunting_counts(
        organization: Optional[str] = None,
        query: Optional[str] = None,
        category: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        time: Optional[str] = None,
        devices: Optional[str] = None,
        filters: Optional[str] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Count threat-hunting results matching a query without retrieving details.

        Useful for dashboards, prevalence analysis, and scoping investigations.

        Args:
            organization: Organization name or None for all.
            query: FortiEDR query language expression.
            category: Telemetry category (Process, Network, File, Registry).
            from_time: ISO-8601 start time.
            to_time: ISO-8601 end time.
            time: Relative time (e.g., '1h', '24h', '7d').
            devices: Comma-separated device names.
            filters: JSON string of additional filters.
            items_per_page: Results per page.
            page_number: Page number.
            sorting: Sort expression.
        """
        return await client.post(
            "/management-rest/threat-hunting/counts",
            json={
                "organization": organization,
                "query": query,
                "category": category,
                "fromTime": from_time,
                "toTime": to_time,
                "time": time,
                "devices": devices,
                "filters": filters,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def threat_hunting_facets(
        facets: str,
        organization: Optional[str] = None,
        query: Optional[str] = None,
        category: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        time: Optional[str] = None,
        devices: Optional[str] = None,
        filters: Optional[str] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Get faceted aggregations of threat-hunting telemetry data.

        Returns grouped/counted values for specified fields, useful for
        building pivot tables and distribution analysis.

        Args:
            facets: Comma-separated field names to aggregate
                (e.g., 'Process.Name,Device.Name').
            organization: Organization name or None for all.
            query: FortiEDR query expression to filter the data before faceting.
            category: Telemetry category to facet on.
            from_time: ISO-8601 start time.
            to_time: ISO-8601 end time.
            time: Relative time (e.g., '1h', '24h', '7d').
            devices: Comma-separated device names.
            filters: JSON string of additional filters.
            items_per_page: Results per page.
            page_number: Page number.
            sorting: Sort expression.
        """
        return await client.post(
            "/management-rest/threat-hunting/facets",
            json={
                "facets": facets,
                "organization": organization,
                "query": query,
                "category": category,
                "fromTime": from_time,
                "toTime": to_time,
                "time": time,
                "devices": devices,
                "filters": filters,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def threat_hunting_list_saved_queries(
        organization: Optional[str] = None,
        scheduled: Optional[bool] = None,
        source: Optional[str] = None,
    ) -> Any:
        """List saved threat-hunting queries.

        Returns user-created and Fortinet-provided saved queries for
        common threat-hunting scenarios.

        Args:
            organization: Organization name or None for all.
            scheduled: If True, return only scheduled queries.
            source: Filter by source: 'Fortinet' for built-in or
                'Custom' for user-created queries.
        """
        return await client.get(
            "/management-rest/threat-hunting/list-saved-queries",
            params={
                "organization": organization,
                "scheduled": scheduled,
                "source": source,
            },
        )

    @mcp.tool()
    async def threat_hunting_save_query(
        name: str,
        query: str,
        category: str,
        organization: Optional[str] = None,
        description: Optional[str] = None,
        classification: Optional[str] = None,
        community: Optional[bool] = None,
        scheduled: Optional[bool] = None,
        frequency: Optional[int] = None,
        frequency_unit: Optional[str] = None,
        hour: Optional[int] = None,
        day_of_week: Optional[int] = None,
        day_of_month: Optional[int] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        time: Optional[str] = None,
        state: Optional[bool] = None,
        force_saving: Optional[bool] = None,
        tag_ids: Optional[str] = None,
        tag_names: Optional[str] = None,
        collector_names: Optional[str] = None,
        query_to_edit: Optional[str] = None,
        edit_id: Optional[int] = None,
    ) -> Any:
        """Save a new threat-hunting query or update an existing one.

        Args:
            name: Name for the saved query.
            query: The FortiEDR query expression.
            category: Telemetry category for the query.
            organization: Organization name or None for all.
            description: Human-readable description of what the query detects.
            classification: Threat classification label for this query.
            community: If True, share with all users in the organization.
            scheduled: If True, run this query on a schedule.
            frequency: Scheduling frequency number.
            frequency_unit: Unit for frequency: 'Hours', 'Days', 'Weeks'.
            hour: Hour of day (0-23) for scheduled execution.
            day_of_week: Day of week (1-7) for weekly schedules.
            day_of_month: Day of month (1-31) for monthly schedules.
            from_time: ISO-8601 start time for query execution range.
            to_time: ISO-8601 end time for query execution range.
            time: Relative time range (e.g., '1h', '24h').
            state: True to enable the query, False to disable.
            force_saving: Force save even if a similar query exists.
            tag_ids: Comma-separated tag IDs to attach to the query.
            tag_names: Comma-separated tag names to attach.
            collector_names: Comma-separated collector names to scope the query.
            query_to_edit: Name of an existing query to edit (update mode).
            edit_id: ID of an existing query to edit (update mode).
        """
        return await client.post(
            "/management-rest/threat-hunting/save-query",
            params={
                "id": edit_id,
                "queryToEdit": query_to_edit,
            },
            json={
                "name": name,
                "query": query,
                "category": category,
                "organization": organization,
                "description": description,
                "classification": classification,
                "community": community,
                "scheduled": scheduled,
                "frequency": frequency,
                "frequencyUnit": frequency_unit,
                "hour": hour,
                "dayOfWeek": day_of_week,
                "dayOfMonth": day_of_month,
                "fromTime": from_time,
                "toTime": to_time,
                "time": time,
                "state": state,
                "forceSaving": force_saving,
                "tagIds": tag_ids,
                "tagNames": tag_names,
                "collectorNames": collector_names,
            },
        )

    @mcp.tool()
    async def threat_hunting_delete_saved_queries(
        organization: Optional[str] = None,
        query_ids: Optional[str] = None,
        query_names: Optional[str] = None,
        scheduled: Optional[bool] = None,
        source: Optional[str] = None,
        delete_all: Optional[bool] = None,
        delete_from_community: Optional[bool] = None,
    ) -> Any:
        """Delete saved threat-hunting queries.

        Args:
            organization: Organization name or None for all.
            query_ids: Comma-separated query IDs to delete.
            query_names: Comma-separated query names to delete.
            scheduled: Delete only scheduled (True) or non-scheduled (False) queries.
            source: Delete only queries from this source ('Fortinet' or 'Custom').
            delete_all: If True, delete all queries matching the filter.
            delete_from_community: If True, also remove from community library.
        """
        return await client.delete(
            "/management-rest/threat-hunting/delete-saved-queries",
            params={
                "organization": organization,
                "queryIds": query_ids,
                "queryNames": query_names,
                "scheduled": scheduled,
                "source": source,
                "deleteAll": delete_all,
                "deleteFromCommunity": delete_from_community,
            },
        )

    @mcp.tool()
    async def threat_hunting_set_query_state(
        state: bool,
        organization: Optional[str] = None,
        query_ids: Optional[str] = None,
        query_names: Optional[str] = None,
        source: Optional[str] = None,
        mark_all: Optional[bool] = None,
    ) -> Any:
        """Enable or disable saved threat-hunting queries.

        Args:
            state: True to enable queries, False to disable.
            organization: Organization name or None for all.
            query_ids: Comma-separated query IDs to update.
            query_names: Comma-separated query names to update.
            source: Filter by source ('Fortinet' or 'Custom').
            mark_all: If True, apply state change to all matching queries.
        """
        return await client.put(
            "/management-rest/threat-hunting/set-query-state",
            params={
                "state": state,
                "organization": organization,
                "queryIds": query_ids,
                "queryNames": query_names,
                "source": source,
                "markAll": mark_all,
            },
        )

    @mcp.tool()
    async def threat_hunting_customize_fortinet_query(
        organization: Optional[str] = None,
        query_id: Optional[int] = None,
        query_to_edit: Optional[str] = None,
        scheduled: Optional[bool] = None,
        state: Optional[bool] = None,
        frequency: Optional[int] = None,
        frequency_unit: Optional[str] = None,
        hour: Optional[int] = None,
        day_of_week: Optional[int] = None,
        day_of_month: Optional[int] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        time: Optional[str] = None,
        force_saving: Optional[bool] = None,
    ) -> Any:
        """Customize a Fortinet built-in threat-hunting query's schedule and state.

        Allows modifying scheduling and activation settings of the predefined
        FortiEDR threat-hunting queries without changing their logic.

        Args:
            organization: Organization name or None for all.
            query_id: ID of the Fortinet query to customize.
            query_to_edit: Name of the Fortinet query to customize.
            scheduled: Enable/disable scheduling for this query.
            state: Enable (True) or disable (False) the query.
            frequency: Scheduling frequency number.
            frequency_unit: Unit: 'Hours', 'Days', or 'Weeks'.
            hour: Hour of day (0-23) for scheduled runs.
            day_of_week: Day of week (1-7) for weekly schedules.
            day_of_month: Day of month (1-31) for monthly schedules.
            from_time: ISO-8601 start time for query range.
            to_time: ISO-8601 end time for query range.
            time: Relative time range (e.g., '24h').
            force_saving: Force save even if changes conflict.
        """
        return await client.post(
            "/management-rest/threat-hunting/customize-fortinet-query",
            params={
                "id": query_id,
                "queryToEdit": query_to_edit,
            },
            json={
                "organization": organization,
                "scheduled": scheduled,
                "state": state,
                "frequency": frequency,
                "frequencyUnit": frequency_unit,
                "hour": hour,
                "dayOfWeek": day_of_week,
                "dayOfMonth": day_of_month,
                "fromTime": from_time,
                "toTime": to_time,
                "time": time,
                "forceSaving": force_saving,
            },
        )

    @mcp.tool()
    async def threat_hunting_list_tags(
        organization: Optional[str] = None,
    ) -> Any:
        """List all tags used to categorize threat-hunting queries.

        Args:
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/threat-hunting/list-tags",
            params={"organization": organization},
        )

    @mcp.tool()
    async def threat_hunting_create_or_edit_tag(
        tag_name: str,
        organization: Optional[str] = None,
        new_tag_name: Optional[str] = None,
        tag_id: Optional[int] = None,
    ) -> Any:
        """Create a new tag or rename an existing tag for threat-hunting queries.

        Args:
            tag_name: Name of the tag to create or current name to rename.
            organization: Organization name or None for all.
            new_tag_name: New name for the tag (if renaming an existing tag).
            tag_id: ID of the tag to edit (for update operations).
        """
        return await client.post(
            "/management-rest/threat-hunting/create-or-edit-tag",
            json={
                "tagName": tag_name,
                "organization": organization,
                "newTagName": new_tag_name,
                "tagId": tag_id,
            },
        )

    @mcp.tool()
    async def threat_hunting_delete_tags(
        organization: Optional[str] = None,
        tag_ids: Optional[str] = None,
        tag_names: Optional[str] = None,
    ) -> Any:
        """Delete threat-hunting query tags.

        Args:
            organization: Organization name or None for all.
            tag_ids: Comma-separated tag IDs to delete.
            tag_names: Comma-separated tag names to delete.
        """
        return await client.delete(
            "/management-rest/threat-hunting/delete-tags",
            params={
                "organization": organization,
                "tagIds": tag_ids,
                "tagNames": tag_names,
            },
        )
