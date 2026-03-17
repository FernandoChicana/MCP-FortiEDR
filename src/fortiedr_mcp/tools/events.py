"""Events tools – list, count, update and delete security events."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)

# Shared event filter param names (used by list, count, update, delete)
_EVENT_FILTER_PARAMS = [
    "actions", "archived", "classifications", "collectorGroups", "destinations",
    "device", "deviceControl", "deviceIps", "eventIds", "eventType", "expired",
    "fileHash", "firstSeenFrom", "firstSeenTo", "handled", "itemsPerPage",
    "lastSeenFrom", "lastSeenTo", "loggedUser", "macAddresses", "muted",
    "operatingSystems", "organization", "pageNumber", "paths", "process",
    "rule", "seen", "severities", "signed", "sorting", "strictMode",
]


def _event_filter(
    organization: Optional[str],
    actions: Optional[str],
    archived: Optional[bool],
    classifications: Optional[str],
    collector_groups: Optional[str],
    destinations: Optional[str],
    device: Optional[str],
    device_control: Optional[bool],
    device_ips: Optional[str],
    event_ids: Optional[str],
    event_type: Optional[str],
    expired: Optional[bool],
    file_hash: Optional[str],
    first_seen_from: Optional[str],
    first_seen_to: Optional[str],
    handled: Optional[bool],
    items_per_page: Optional[int],
    last_seen_from: Optional[str],
    last_seen_to: Optional[str],
    logged_user: Optional[str],
    mac_addresses: Optional[str],
    muted: Optional[bool],
    operating_systems: Optional[str],
    page_number: Optional[int],
    paths: Optional[str],
    process: Optional[str],
    rule: Optional[str],
    seen: Optional[bool],
    severities: Optional[str],
    signed: Optional[bool],
    sorting: Optional[str],
    strict_mode: Optional[bool],
) -> dict:
    return {
        "organization": organization,
        "actions": actions,
        "archived": archived,
        "classifications": classifications,
        "collectorGroups": collector_groups,
        "destinations": destinations,
        "device": device,
        "deviceControl": device_control,
        "deviceIps": device_ips,
        "eventIds": event_ids,
        "eventType": event_type,
        "expired": expired,
        "fileHash": file_hash,
        "firstSeenFrom": first_seen_from,
        "firstSeenTo": first_seen_to,
        "handled": handled,
        "itemsPerPage": items_per_page,
        "lastSeenFrom": last_seen_from,
        "lastSeenTo": last_seen_to,
        "loggedUser": logged_user,
        "macAddresses": mac_addresses,
        "muted": muted,
        "operatingSystems": operating_systems,
        "pageNumber": page_number,
        "paths": paths,
        "process": process,
        "rule": rule,
        "seen": seen,
        "severities": severities,
        "signed": signed,
        "sorting": sorting,
        "strictMode": strict_mode,
    }


def register(mcp: FastMCP) -> None:
    """Register all events tools on the given FastMCP instance."""

    @mcp.tool()
    async def events_list_events(
        organization: Optional[str] = None,
        event_ids: Optional[str] = None,
        severities: Optional[str] = None,
        classifications: Optional[str] = None,
        actions: Optional[str] = None,
        device: Optional[str] = None,
        device_ips: Optional[str] = None,
        collector_groups: Optional[str] = None,
        operating_systems: Optional[str] = None,
        destinations: Optional[str] = None,
        paths: Optional[str] = None,
        process: Optional[str] = None,
        rule: Optional[str] = None,
        file_hash: Optional[str] = None,
        logged_user: Optional[str] = None,
        mac_addresses: Optional[str] = None,
        event_type: Optional[str] = None,
        first_seen_from: Optional[str] = None,
        first_seen_to: Optional[str] = None,
        last_seen_from: Optional[str] = None,
        last_seen_to: Optional[str] = None,
        handled: Optional[bool] = None,
        seen: Optional[bool] = None,
        archived: Optional[bool] = None,
        muted: Optional[bool] = None,
        expired: Optional[bool] = None,
        device_control: Optional[bool] = None,
        signed: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """List FortiEDR security events with rich filtering and pagination.

        Returns a paginated list of security events detected by FortiEDR
        collectors, with full event metadata including severity, classification,
        process information, and timeline.

        Args:
            organization: Organization name or None for all.
            event_ids: Comma-separated event IDs to retrieve specifically.
            severities: Comma-separated severity levels (Critical, High, Medium, Low, Info).
            classifications: Comma-separated event classifications
                (e.g., 'Ransomware', 'Malware', 'Suspicious Activity').
            actions: Comma-separated actions taken (e.g., 'Block', 'Simulate').
            device: Filter by device name (hostname).
            device_ips: Comma-separated device IP addresses to filter.
            collector_groups: Comma-separated collector group names.
            operating_systems: Comma-separated OS names/versions.
            destinations: Comma-separated destination IPs or hostnames.
            paths: Comma-separated file paths involved in the event.
            process: Process name filter.
            rule: Rule name that triggered the event.
            file_hash: SHA256 or MD5 hash of the file involved.
            logged_user: Windows username logged in when the event occurred.
            mac_addresses: Comma-separated MAC addresses.
            event_type: Type of event (e.g., 'Threat', 'DeviceControl').
            first_seen_from: ISO-8601 start datetime for first-seen filter.
            first_seen_to: ISO-8601 end datetime for first-seen filter.
            last_seen_from: ISO-8601 start datetime for last-seen filter.
            last_seen_to: ISO-8601 end datetime for last-seen filter.
            handled: True = handled events only; False = unhandled only.
            seen: True = read events; False = unread events.
            archived: True = archived events; False = active events.
            muted: True = muted events; False = unmuted events.
            expired: True = expired events; False = current events.
            device_control: True = device control events only.
            signed: True = events involving signed files; False = unsigned.
            strict_mode: True for exact match on all string filters.
            items_per_page: Number of results per page (default varies).
            page_number: Page number to retrieve (1-based).
            sorting: Sort expression, e.g. 'firstSeen desc'.
        """
        return await client.get(
            "/management-rest/events/list-events",
            params=_event_filter(
                organization=organization, actions=actions, archived=archived,
                classifications=classifications, collector_groups=collector_groups,
                destinations=destinations, device=device,
                device_control=device_control, device_ips=device_ips,
                event_ids=event_ids, event_type=event_type, expired=expired,
                file_hash=file_hash, first_seen_from=first_seen_from,
                first_seen_to=first_seen_to, handled=handled,
                items_per_page=items_per_page, last_seen_from=last_seen_from,
                last_seen_to=last_seen_to, logged_user=logged_user,
                mac_addresses=mac_addresses, muted=muted,
                operating_systems=operating_systems, page_number=page_number,
                paths=paths, process=process, rule=rule, seen=seen,
                severities=severities, signed=signed, sorting=sorting,
                strict_mode=strict_mode,
            ),
        )

    @mcp.tool()
    async def events_count_events(
        organization: Optional[str] = None,
        severities: Optional[str] = None,
        classifications: Optional[str] = None,
        actions: Optional[str] = None,
        device: Optional[str] = None,
        device_ips: Optional[str] = None,
        collector_groups: Optional[str] = None,
        operating_systems: Optional[str] = None,
        destinations: Optional[str] = None,
        paths: Optional[str] = None,
        process: Optional[str] = None,
        rule: Optional[str] = None,
        file_hash: Optional[str] = None,
        logged_user: Optional[str] = None,
        mac_addresses: Optional[str] = None,
        event_type: Optional[str] = None,
        event_ids: Optional[str] = None,
        first_seen_from: Optional[str] = None,
        first_seen_to: Optional[str] = None,
        last_seen_from: Optional[str] = None,
        last_seen_to: Optional[str] = None,
        handled: Optional[bool] = None,
        seen: Optional[bool] = None,
        archived: Optional[bool] = None,
        muted: Optional[bool] = None,
        expired: Optional[bool] = None,
        device_control: Optional[bool] = None,
        signed: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """Count FortiEDR security events matching the given filter criteria.

        Returns the total number of events matching the filter without
        retrieving the full event details. Useful for dashboards and metrics.

        Args:
            organization: Organization name or None for all.
            severities: Comma-separated severity levels to count.
            classifications: Comma-separated event classifications.
            actions: Comma-separated actions taken.
            device: Device name (hostname) filter.
            device_ips: Comma-separated device IP addresses.
            collector_groups: Comma-separated collector group names.
            operating_systems: Comma-separated OS names.
            destinations: Comma-separated destination IPs or hostnames.
            paths: Comma-separated file paths.
            process: Process name filter.
            rule: Rule name filter.
            file_hash: File hash (SHA256/MD5) filter.
            logged_user: Windows username filter.
            mac_addresses: Comma-separated MAC addresses.
            event_type: Event type filter.
            event_ids: Comma-separated specific event IDs.
            first_seen_from: ISO-8601 start for first-seen range.
            first_seen_to: ISO-8601 end for first-seen range.
            last_seen_from: ISO-8601 start for last-seen range.
            last_seen_to: ISO-8601 end for last-seen range.
            handled: Filter by handled status.
            seen: Filter by read/unread status.
            archived: Filter by archived status.
            muted: Filter by muted status.
            expired: Filter by expired status.
            device_control: Filter to device control events only.
            signed: Filter by signed/unsigned file status.
            strict_mode: Use exact matching for string filters.
            items_per_page: Unused for count but included for API compatibility.
            page_number: Unused for count but included for API compatibility.
            sorting: Sort expression.
        """
        return await client.get(
            "/management-rest/events/count-events",
            params=_event_filter(
                organization=organization, actions=actions, archived=archived,
                classifications=classifications, collector_groups=collector_groups,
                destinations=destinations, device=device,
                device_control=device_control, device_ips=device_ips,
                event_ids=event_ids, event_type=event_type, expired=expired,
                file_hash=file_hash, first_seen_from=first_seen_from,
                first_seen_to=first_seen_to, handled=handled,
                items_per_page=items_per_page, last_seen_from=last_seen_from,
                last_seen_to=last_seen_to, logged_user=logged_user,
                mac_addresses=mac_addresses, muted=muted,
                operating_systems=operating_systems, page_number=page_number,
                paths=paths, process=process, rule=rule, seen=seen,
                severities=severities, signed=signed, sorting=sorting,
                strict_mode=strict_mode,
            ),
        )

    @mcp.tool()
    async def events_create_exception(
        event_id: int,
        organization: Optional[str] = None,
        exception_id: Optional[int] = None,
        comment: Optional[str] = None,
        all_collector_groups: Optional[bool] = None,
        all_destinations: Optional[bool] = None,
        all_organizations: Optional[bool] = None,
        all_users: Optional[bool] = None,
        collector_groups: Optional[str] = None,
        destinations: Optional[str] = None,
        users: Optional[str] = None,
        force_create: Optional[bool] = None,
        use_any_path: Optional[str] = None,
        use_in_exception: Optional[str] = None,
        wildcard_files: Optional[str] = None,
        wildcard_paths: Optional[str] = None,
    ) -> Any:
        """Create an exception for a specific security event to prevent future alerts.

        Generates a FortiEDR exception that whitelists the event pattern so
        similar benign events are suppressed in the future.

        Args:
            event_id: ID of the event to create an exception for.
            organization: Organization name or None for all.
            exception_id: If updating an existing exception, provide its ID.
            comment: Optional explanation for creating this exception.
            all_collector_groups: If True, apply to all collector groups.
            all_destinations: If True, apply to all destination IPs.
            all_organizations: If True, apply across all organizations.
            all_users: If True, apply for all users.
            collector_groups: Comma-separated specific collector groups.
            destinations: Comma-separated specific destination IPs.
            users: Comma-separated specific usernames.
            force_create: Force creation even if a similar exception exists.
            use_any_path: Wildcard path matching option.
            use_in_exception: Fields to include in the exception definition.
            wildcard_files: Wildcard patterns for filenames.
            wildcard_paths: Wildcard patterns for file paths.
        """
        return await client.post(
            "/management-rest/events/create-exception",
            params={
                "eventId": event_id,
                "exceptionId": exception_id,
                "organization": organization,
                "comment": comment,
                "allCollectorGroups": all_collector_groups,
                "allDestinations": all_destinations,
                "allOrganizations": all_organizations,
                "allUsers": all_users,
                "collectorGroups": collector_groups,
                "destinations": destinations,
                "users": users,
                "forceCreate": force_create,
            },
            json={
                "useAnyPath": use_any_path,
                "useInException": use_in_exception,
                "wildcardFiles": wildcard_files,
                "wildcardPaths": wildcard_paths,
            },
        )

    @mcp.tool()
    async def events_list_raw_data_items(
        event_id: Optional[int] = None,
        organization: Optional[str] = None,
        collector_groups: Optional[str] = None,
        destinations: Optional[str] = None,
        device: Optional[str] = None,
        device_ips: Optional[str] = None,
        raw_event_ids: Optional[str] = None,
        logged_user: Optional[str] = None,
        first_seen_from: Optional[str] = None,
        first_seen_to: Optional[str] = None,
        last_seen_from: Optional[str] = None,
        last_seen_to: Optional[str] = None,
        full_data_requested: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        items_per_page: Optional[int] = None,
        page_number: Optional[int] = None,
        sorting: Optional[str] = None,
    ) -> Any:
        """List raw data items (individual event occurrences) for a security event.

        Returns the granular telemetry records associated with a specific event,
        including process trees, network connections, and file operations.

        Args:
            event_id: Parent event ID to list raw items for.
            organization: Organization name or None for all.
            collector_groups: Comma-separated collector group names.
            destinations: Comma-separated destination IPs/hostnames.
            device: Device hostname filter.
            device_ips: Comma-separated device IP addresses.
            raw_event_ids: Comma-separated raw event IDs to retrieve.
            logged_user: Windows username filter.
            first_seen_from: ISO-8601 start for first-seen filter.
            first_seen_to: ISO-8601 end for first-seen filter.
            last_seen_from: ISO-8601 start for last-seen filter.
            last_seen_to: ISO-8601 end for last-seen filter.
            full_data_requested: If True, return full telemetry data.
            strict_mode: Use exact matching for string filters.
            items_per_page: Results per page.
            page_number: Page number (1-based).
            sorting: Sort expression.
        """
        return await client.get(
            "/management-rest/events/list-raw-data-items",
            params={
                "eventId": event_id,
                "organization": organization,
                "collectorGroups": collector_groups,
                "destinations": destinations,
                "device": device,
                "deviceIps": device_ips,
                "rawEventIds": raw_event_ids,
                "loggedUser": logged_user,
                "firstSeenFrom": first_seen_from,
                "firstSeenTo": first_seen_to,
                "lastSeenFrom": last_seen_from,
                "lastSeenTo": last_seen_to,
                "fullDataRequested": full_data_requested,
                "strictMode": strict_mode,
                "itemsPerPage": items_per_page,
                "pageNumber": page_number,
                "sorting": sorting,
            },
        )

    @mcp.tool()
    async def events_export_raw_data_items_json(
        raw_item_ids: str,
        organization: Optional[str] = None,
    ) -> Any:
        """Export specific raw event data items as JSON.

        Returns the full structured JSON representation of the specified raw
        event telemetry items, suitable for SIEM ingestion or forensic analysis.

        Args:
            raw_item_ids: Comma-separated raw event item IDs to export.
            organization: Organization name or None for all.
        """
        return await client.get(
            "/management-rest/events/export-raw-data-items-json",
            params={
                "rawItemIds": raw_item_ids,
                "organization": organization,
            },
        )

    @mcp.tool()
    async def events_update_events(
        organization: Optional[str] = None,
        event_ids: Optional[str] = None,
        severities: Optional[str] = None,
        classifications: Optional[str] = None,
        actions: Optional[str] = None,
        device: Optional[str] = None,
        collector_groups: Optional[str] = None,
        first_seen_from: Optional[str] = None,
        first_seen_to: Optional[str] = None,
        last_seen_from: Optional[str] = None,
        last_seen_to: Optional[str] = None,
        handled: Optional[bool] = None,
        archived: Optional[bool] = None,
        muted: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
        # Update actions
        handle: Optional[bool] = None,
        archive: Optional[bool] = None,
        mute: Optional[bool] = None,
        force_unmute: Optional[bool] = None,
        read: Optional[bool] = None,
        classification: Optional[str] = None,
        comment: Optional[str] = None,
        family_name: Optional[str] = None,
        threat_name: Optional[str] = None,
        malware_type: Optional[str] = None,
        mute_duration: Optional[str] = None,
    ) -> Any:
        """Update the state of one or more FortiEDR security events.

        Supports bulk operations: mark as handled/unhandled, archive, mute,
        mark as read/unread, and set classification metadata.

        Args:
            organization: Organization name or None for all.
            event_ids: Comma-separated event IDs to update.
            severities: Filter events by severity before updating.
            classifications: Filter by current classification.
            actions: Filter by action taken.
            device: Filter by device hostname.
            collector_groups: Filter by collector group names.
            first_seen_from: Filter by first-seen start (ISO-8601).
            first_seen_to: Filter by first-seen end (ISO-8601).
            last_seen_from: Filter by last-seen start (ISO-8601).
            last_seen_to: Filter by last-seen end (ISO-8601).
            handled: Filter by current handled status.
            archived: Filter by current archived status.
            muted: Filter by current muted status.
            strict_mode: Use exact matching for string filters.
            handle: Set to True to mark matched events as handled.
            archive: Set to True to archive matched events.
            mute: Set to True to mute matched events.
            force_unmute: Set to True to forcibly unmute events.
            read: Set to True to mark events as read.
            classification: New classification label to apply.
            comment: Comment to add to the events.
            family_name: Malware family name to assign.
            threat_name: Threat name to assign.
            malware_type: Malware type classification.
            mute_duration: Duration string for muting (e.g., '1d', '1w').
        """
        return await client.put(
            "/management-rest/events",
            params=_event_filter(
                organization=organization, actions=actions, archived=archived,
                classifications=classifications, collector_groups=collector_groups,
                destinations=None, device=device, device_control=None,
                device_ips=None, event_ids=event_ids, event_type=None,
                expired=None, file_hash=None, first_seen_from=first_seen_from,
                first_seen_to=first_seen_to, handled=handled,
                items_per_page=None, last_seen_from=last_seen_from,
                last_seen_to=last_seen_to, logged_user=None,
                mac_addresses=None, muted=muted, operating_systems=None,
                page_number=None, paths=None, process=None, rule=None,
                seen=None, severities=severities, signed=None, sorting=None,
                strict_mode=strict_mode,
            ),
            json={
                "handle": handle,
                "archive": archive,
                "mute": mute,
                "forceUnmute": force_unmute,
                "read": read,
                "classification": classification,
                "comment": comment,
                "familyName": family_name,
                "threatName": threat_name,
                "malwareType": malware_type,
                "muteDuration": mute_duration,
            },
        )

    @mcp.tool()
    async def events_delete_events(
        organization: Optional[str] = None,
        event_ids: Optional[str] = None,
        severities: Optional[str] = None,
        classifications: Optional[str] = None,
        device: Optional[str] = None,
        collector_groups: Optional[str] = None,
        first_seen_from: Optional[str] = None,
        first_seen_to: Optional[str] = None,
        last_seen_from: Optional[str] = None,
        last_seen_to: Optional[str] = None,
        handled: Optional[bool] = None,
        archived: Optional[bool] = None,
        delete_all: Optional[bool] = None,
        strict_mode: Optional[bool] = None,
    ) -> Any:
        """Permanently delete FortiEDR security events matching the filter.

        WARNING: This operation is irreversible. Deleted events cannot be
        recovered. Use filters carefully to avoid unintended bulk deletions.

        Args:
            organization: Organization name or None for all.
            event_ids: Comma-separated specific event IDs to delete.
            severities: Delete only events with these severity levels.
            classifications: Delete only events with these classifications.
            device: Delete only events from this device hostname.
            collector_groups: Delete only events from these collector groups.
            first_seen_from: Delete events first seen after this ISO-8601 datetime.
            first_seen_to: Delete events first seen before this ISO-8601 datetime.
            last_seen_from: Delete events last seen after this ISO-8601 datetime.
            last_seen_to: Delete events last seen before this ISO-8601 datetime.
            handled: Delete only handled (True) or unhandled (False) events.
            archived: Delete only archived (True) or active (False) events.
            delete_all: If True, delete ALL events matching the filter (use with care).
            strict_mode: Use exact matching for string filters.
        """
        return await client.delete(
            "/management-rest/events",
            params={
                "organization": organization,
                "eventIds": event_ids,
                "severities": severities,
                "classifications": classifications,
                "device": device,
                "collectorGroups": collector_groups,
                "firstSeenFrom": first_seen_from,
                "firstSeenTo": first_seen_to,
                "lastSeenFrom": last_seen_from,
                "lastSeenTo": last_seen_to,
                "handled": handled,
                "archived": archived,
                "deleteAll": delete_all,
                "strictMode": strict_mode,
            },
        )
