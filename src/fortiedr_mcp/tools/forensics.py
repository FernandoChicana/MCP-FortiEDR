"""Forensics tools – file retrieval and device remediation."""

import logging
from typing import Any, Optional

from fastmcp import FastMCP

from ..api.client import client

logger = logging.getLogger(__name__)


def register(mcp: FastMCP) -> None:
    """Register all forensics tools on the given FastMCP instance."""

    @mcp.tool()
    async def forensics_get_event_file(
        raw_event_id: int,
        organization: Optional[str] = None,
        file_paths: Optional[str] = None,
        disk: Optional[bool] = None,
        memory: Optional[bool] = None,
        process_id: Optional[int] = None,
        start_range: Optional[str] = None,
        end_range: Optional[str] = None,
    ) -> Any:
        """Retrieve a file or memory dump associated with a specific event.

        Fetches the actual file artifact or memory region captured during a
        security event for forensic analysis.

        Args:
            raw_event_id: The raw event ID to retrieve the file for.
            organization: Organization name or None for all.
            file_paths: Comma-separated file paths to retrieve from the event.
            disk: If True, retrieve the file from disk.
            memory: If True, retrieve a memory dump.
            process_id: Process ID for memory dump retrieval.
            start_range: Start offset for partial file/memory retrieval.
            end_range: End offset for partial file/memory retrieval.
        """
        return await client.get(
            "/management-rest/forensics/get-event-file",
            params={
                "rawEventId": raw_event_id,
                "organization": organization,
                "filePaths": file_paths,
                "disk": disk,
                "memory": memory,
                "processId": process_id,
                "startRange": start_range,
                "endRange": end_range,
            },
        )

    @mcp.tool()
    async def forensics_get_file(
        device: str,
        file_paths: str,
        organization: Optional[str] = None,
        type: Optional[str] = None,
    ) -> Any:
        """Retrieve a file or memory artifact directly from a live device.

        Fetches a file from a collector-monitored endpoint for forensic
        investigation without needing an associated event.

        Args:
            device: Hostname of the device to retrieve the file from.
            file_paths: Comma-separated file paths to retrieve.
            organization: Organization name or None for all.
            type: Type of retrieval: 'File' or 'Memory'.
        """
        return await client.get(
            "/management-rest/forensics/get-file",
            params={
                "device": device,
                "filePaths": file_paths,
                "organization": organization,
                "type": type,
            },
        )

    @mcp.tool()
    async def forensics_remediate_device(
        device: str,
        organization: Optional[str] = None,
        device_id: Optional[int] = None,
        process_name: Optional[str] = None,
        terminated_process_id: Optional[int] = None,
        thread_id: Optional[int] = None,
        executables_to_remove: Optional[str] = None,
        persistence_data_action: Optional[str] = None,
        persistence_data_path: Optional[str] = None,
        persistence_data_value_name: Optional[str] = None,
        persistence_data_new_content: Optional[str] = None,
        persistence_data_value_new_type: Optional[str] = None,
    ) -> Any:
        """Perform live remediation on a compromised device.

        Supports killing processes, deleting malicious files, and cleaning
        persistence mechanisms (registry keys, startup entries, etc.) on a
        FortiEDR-monitored endpoint.

        Args:
            device: Hostname of the device to remediate.
            organization: Organization name or None for all.
            device_id: Numeric device ID (alternative to hostname).
            process_name: Name of the process to terminate.
            terminated_process_id: PID of the specific process to kill.
            thread_id: Thread ID to target within a process.
            executables_to_remove: Comma-separated file paths of executables
                to delete from the device.
            persistence_data_action: Action for persistence cleanup:
                'Delete', 'Modify', etc.
            persistence_data_path: Registry or file path of the persistence entry.
            persistence_data_value_name: Registry value name to modify/delete.
            persistence_data_new_content: New content to write (for Modify action).
            persistence_data_value_new_type: New registry value type.
        """
        return await client.put(
            "/management-rest/forensics/remediate-device",
            params={
                "device": device,
                "organization": organization,
                "deviceId": device_id,
                "processName": process_name,
                "terminatedProcessId": terminated_process_id,
                "threadId": thread_id,
                "executablesToRemove": executables_to_remove,
                "persistenceDataAction": persistence_data_action,
                "persistenceDataPath": persistence_data_path,
                "persistenceDataValueName": persistence_data_value_name,
                "persistenceDataNewContent": persistence_data_new_content,
                "persistenceDataValueNewType": persistence_data_value_new_type,
            },
        )
