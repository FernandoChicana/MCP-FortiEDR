"""Async HTTP client for the FortiEDR REST API.

A single FortiEDRClient instance is shared by all tool functions.
Authentication is Basic Auth; SSL verification is configurable.
"""

import logging
import ssl
from typing import Any, Optional

import aiohttp

from ..utils.config import settings

logger = logging.getLogger(__name__)


class FortiEDRError(Exception):
    """Base exception for FortiEDR API errors."""


class AuthenticationError(FortiEDRError):
    """Raised when the server returns 401 Unauthorized."""


class APIError(FortiEDRError):
    """Raised for 4xx/5xx HTTP responses other than 401."""

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        super().__init__(f"HTTP {status}: {message}")


class ConnectionError(FortiEDRError):
    """Raised when the server cannot be reached."""


class FortiEDRClient:
    """Async HTTP client for FortiEDR REST API.

    Uses aiohttp with Basic Auth. One instance per container (one FortiEDR host).
    The session is lazily created on first use and reused across requests.
    """

    def __init__(self) -> None:
        self.base_url = (
            f"https://{settings.fortiedr_host}:{settings.fortiedr_port}"
        )
        self._auth = aiohttp.BasicAuth(
            settings.fortiedr_user, settings.fortiedr_password
        )
        self._verify_ssl: bool = settings.fortiedr_verify_ssl
        self._session: Optional[aiohttp.ClientSession] = None

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            ssl_ctx: Any
            if self._verify_ssl:
                ssl_ctx = ssl.create_default_context()
            else:
                ssl_ctx = False  # disable SSL verification

            connector = aiohttp.TCPConnector(ssl=ssl_ctx)
            self._session = aiohttp.ClientSession(
                auth=self._auth,
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=60, connect=10),
                headers={"Accept": "application/json"},
            )
        return self._session

    async def close(self) -> None:
        """Close the underlying aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    # ------------------------------------------------------------------
    # Core request method
    # ------------------------------------------------------------------

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        data: Optional[Any] = None,
    ) -> Any:
        """Send an authenticated HTTP request to FortiEDR.

        Args:
            method: HTTP verb (GET, POST, PUT, DELETE).
            path: API path, e.g. '/management-rest/events/list-events'.
            params: Query parameters (None values are stripped).
            json: JSON request body (None values are stripped).
            data: Raw form data (for multipart uploads).

        Returns:
            Parsed JSON response, or raw text if response is not JSON.

        Raises:
            AuthenticationError: On HTTP 401.
            APIError: On other HTTP error codes.
            ConnectionError: When the host is unreachable.
        """
        session = await self._get_session()
        url = f"{self.base_url}{path}"

        # Strip None values so optional params don't pollute the request
        clean_params = (
            {k: v for k, v in params.items() if v is not None} if params else None
        )
        clean_json = (
            {k: v for k, v in json.items() if v is not None} if json else None
        )

        logger.info("%s %s params=%s", method, url, clean_params)

        try:
            async with session.request(
                method,
                url,
                params=clean_params,
                json=clean_json if not data else None,
                data=data,
            ) as resp:
                if resp.status == 401:
                    logger.error("Authentication failed for %s", url)
                    raise AuthenticationError(
                        "Authentication failed – check FORTIEDR_USER / FORTIEDR_PASSWORD"
                    )

                if resp.status >= 400:
                    body = await resp.text()
                    logger.error("HTTP %d from %s: %s", resp.status, url, body[:500])
                    raise APIError(resp.status, body[:500])

                content_type = resp.headers.get("Content-Type", "")
                if "json" in content_type:
                    return await resp.json(content_type=None)
                return await resp.text()

        except aiohttp.ClientConnectorError as exc:
            logger.error("Connection error to %s: %s", url, exc)
            raise ConnectionError(
                f"Cannot connect to FortiEDR at {self.base_url}: {exc}"
            ) from exc
        except aiohttp.ServerTimeoutError as exc:
            logger.error("Timeout for %s: %s", url, exc)
            raise ConnectionError(f"Request timed out for {url}") from exc

    # ------------------------------------------------------------------
    # Convenience wrappers
    # ------------------------------------------------------------------

    async def get(self, path: str, params: Optional[dict] = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        data: Optional[Any] = None,
    ) -> Any:
        return await self.request("POST", path, params=params, json=json, data=data)

    async def put(
        self,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        return await self.request("PUT", path, params=params, json=json)

    async def delete(
        self,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        return await self.request("DELETE", path, params=params, json=json)

    # ------------------------------------------------------------------
    # Connectivity check (used by health endpoint)
    # ------------------------------------------------------------------

    async def check_connectivity(self) -> bool:
        """Verify that FortiEDR is reachable and credentials are valid."""
        try:
            await self.get("/management-rest/admin/ready")
            return True
        except Exception as exc:
            logger.warning("FortiEDR connectivity check failed: %s", exc)
            return False


# Module-level singleton – shared by all tool functions
client = FortiEDRClient()
