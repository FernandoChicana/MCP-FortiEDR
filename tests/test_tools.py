"""Unit tests for FortiEDR MCP tools.

Tests use mocking to avoid requiring a real FortiEDR instance.
Run with: pytest tests/ -v
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_client_mock(return_value=None):
    """Return a mock FortiEDRClient with get/post/put/delete all mocked."""
    mock = MagicMock()
    mock.get = AsyncMock(return_value=return_value or {"status": "ok"})
    mock.post = AsyncMock(return_value=return_value or {"status": "ok"})
    mock.put = AsyncMock(return_value=return_value or {"status": "ok"})
    mock.delete = AsyncMock(return_value=return_value or {"status": "ok"})
    mock.check_connectivity = AsyncMock(return_value=True)
    return mock


# ---------------------------------------------------------------------------
# Config tests
# ---------------------------------------------------------------------------

class TestSettings:
    def test_settings_load(self, monkeypatch):
        """Settings should load from environment variables."""
        monkeypatch.setenv("FORTIEDR_HOST", "test.example.com")
        monkeypatch.setenv("FORTIEDR_USER", "apiuser")
        monkeypatch.setenv("FORTIEDR_PASSWORD", "secret")

        # Re-import to pick up env changes
        from importlib import reload
        import fortiedr_mcp.utils.config as cfg_module
        reload(cfg_module)

        assert cfg_module.settings.fortiedr_host == "test.example.com"
        assert cfg_module.settings.fortiedr_user == "apiuser"
        assert cfg_module.settings.fortiedr_port == 443
        assert cfg_module.settings.fortiedr_verify_ssl is False
        assert cfg_module.settings.mcp_server_port == 8000

    def test_custom_port(self, monkeypatch):
        monkeypatch.setenv("FORTIEDR_HOST", "host")
        monkeypatch.setenv("FORTIEDR_USER", "u")
        monkeypatch.setenv("FORTIEDR_PASSWORD", "p")
        monkeypatch.setenv("FORTIEDR_PORT", "8443")

        from importlib import reload
        import fortiedr_mcp.utils.config as cfg_module
        reload(cfg_module)

        assert cfg_module.settings.fortiedr_port == 8443


# ---------------------------------------------------------------------------
# Client tests
# ---------------------------------------------------------------------------

class TestFortiEDRClient:
    @pytest.mark.asyncio
    async def test_check_connectivity_success(self):
        from fortiedr_mcp.api.client import FortiEDRClient
        cli = FortiEDRClient.__new__(FortiEDRClient)
        cli.base_url = "https://fake-host:443"
        cli._auth = MagicMock()
        cli._verify_ssl = False
        cli._session = None

        with patch.object(cli, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = {"status": "ready"}
            result = await cli.check_connectivity()
            assert result is True
            mock_get.assert_called_once_with("/management-rest/admin/ready")

    @pytest.mark.asyncio
    async def test_check_connectivity_failure(self):
        from fortiedr_mcp.api.client import FortiEDRClient, ConnectionError
        cli = FortiEDRClient.__new__(FortiEDRClient)
        cli.base_url = "https://fake-host:443"
        cli._auth = MagicMock()
        cli._verify_ssl = False
        cli._session = None

        with patch.object(cli, "get", new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = ConnectionError("unreachable")
            result = await cli.check_connectivity()
            assert result is False


# ---------------------------------------------------------------------------
# Tool registration tests
# ---------------------------------------------------------------------------

class TestToolRegistration:
    def test_all_modules_have_register(self):
        """Every tool module must expose a register() function."""
        from fortiedr_mcp.tools import _MODULES
        for module in _MODULES:
            assert hasattr(module, "register"), (
                f"Module {module.__name__} is missing register()"
            )
            assert callable(module.register)

    def test_register_all_creates_tools(self):
        """register_all() should register tools on a FastMCP instance."""
        from fastmcp import FastMCP
        from fortiedr_mcp.tools import register_all

        mcp = FastMCP("test")
        register_all(mcp)

        # FastMCP stores tools; verify at least some were registered
        # The exact attribute depends on FastMCP version
        tool_count = len(mcp._tool_manager._tools)
        assert tool_count > 50, (
            f"Expected >50 tools, got {tool_count}"
        )


# ---------------------------------------------------------------------------
# Individual tool call tests
# ---------------------------------------------------------------------------

class TestAdminTools:
    @pytest.mark.asyncio
    async def test_list_collector_installers(self):
        mock_response = {
            "availableCollectorInstallers": [
                {"osFamily": "Windows", "version": "5.0.0"}
            ]
        }
        with patch("fortiedr_mcp.tools.admin.client") as mock_client:
            mock_client.get = AsyncMock(return_value=mock_response)

            from fastmcp import FastMCP
            from fortiedr_mcp.tools.admin import register
            mcp = FastMCP("test")
            register(mcp)

            # Verify the tool is registered
            assert "admin_list_collector_installers" in mcp._tool_manager._tools

    @pytest.mark.asyncio
    async def test_ready_endpoint(self):
        with patch("fortiedr_mcp.tools.admin.client") as mock_client:
            mock_client.get = AsyncMock(return_value={"ready": True})

            from fastmcp import FastMCP
            from fortiedr_mcp.tools.admin import register
            mcp = FastMCP("test")
            register(mcp)

            assert "admin_ready" in mcp._tool_manager._tools


class TestEventsTools:
    @pytest.mark.asyncio
    async def test_list_events_calls_correct_endpoint(self):
        with patch("fortiedr_mcp.tools.events.client") as mock_client:
            mock_client.get = AsyncMock(return_value={"events": [], "total": 0})

            from fastmcp import FastMCP
            from fortiedr_mcp.tools.events import register
            mcp = FastMCP("test")
            register(mcp)

            assert "events_list_events" in mcp._tool_manager._tools
            assert "events_count_events" in mcp._tool_manager._tools
            assert "events_update_events" in mcp._tool_manager._tools
            assert "events_delete_events" in mcp._tool_manager._tools

    @pytest.mark.asyncio
    async def test_list_events_passes_org_param(self):
        with patch("fortiedr_mcp.tools.events.client") as mock_client:
            mock_client.get = AsyncMock(return_value=[])

            from fastmcp import FastMCP
            from fortiedr_mcp.tools.events import register
            mcp = FastMCP("test")
            register(mcp)

            tool = mcp._tool_manager._tools["events_list_events"]
            await tool.fn(organization="TestOrg", severities="Critical")

            call_kwargs = mock_client.get.call_args
            assert call_kwargs[1]["params"]["organization"] == "TestOrg"
            assert call_kwargs[1]["params"]["severities"] == "Critical"


class TestInventoryTools:
    @pytest.mark.asyncio
    async def test_isolate_collector_calls_put(self):
        with patch("fortiedr_mcp.tools.inventory.client") as mock_client:
            mock_client.put = AsyncMock(return_value={"success": True})

            from fastmcp import FastMCP
            from fortiedr_mcp.tools.inventory import register
            mcp = FastMCP("test")
            register(mcp)

            tool = mcp._tool_manager._tools["inventory_isolate_collectors"]
            await tool.fn(devices="workstation01", organization="Acme")

            mock_client.put.assert_called_once()
            call_params = mock_client.put.call_args[1]["params"]
            assert call_params["devices"] == "workstation01"
            assert call_params["organization"] == "Acme"


class TestForensicsTools:
    @pytest.mark.asyncio
    async def test_remediate_device_tool_registered(self):
        from fastmcp import FastMCP
        from fortiedr_mcp.tools.forensics import register
        mcp = FastMCP("test")
        register(mcp)
        assert "forensics_remediate_device" in mcp._tool_manager._tools


class TestThreatHuntingTools:
    def test_all_threat_hunting_tools_registered(self):
        from fastmcp import FastMCP
        from fortiedr_mcp.tools.threat_hunting import register
        mcp = FastMCP("test")
        register(mcp)

        expected = [
            "threat_hunting_search",
            "threat_hunting_counts",
            "threat_hunting_facets",
            "threat_hunting_list_saved_queries",
            "threat_hunting_save_query",
            "threat_hunting_delete_saved_queries",
            "threat_hunting_set_query_state",
            "threat_hunting_customize_fortinet_query",
            "threat_hunting_list_tags",
            "threat_hunting_create_or_edit_tag",
            "threat_hunting_delete_tags",
        ]
        for name in expected:
            assert name in mcp._tool_manager._tools, f"Missing tool: {name}"


# ---------------------------------------------------------------------------
# Health endpoint test
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    @pytest.mark.asyncio
    async def test_health_returns_ok_when_connected(self):
        from fastmcp import FastMCP
        from fortiedr_mcp.tools import register_all
        import fortiedr_mcp.server as server_module

        with patch.object(server_module.client, "check_connectivity",
                          new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = True

            mock_request = MagicMock()
            response = await server_module.health_handler(mock_request)

            assert response.status_code == 200
            import json
            body = json.loads(response.body)
            assert body["status"] == "ok"
            assert body["fortiedr_connected"] is True

    @pytest.mark.asyncio
    async def test_health_returns_503_when_disconnected(self):
        import fortiedr_mcp.server as server_module

        with patch.object(server_module.client, "check_connectivity",
                          new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = False

            mock_request = MagicMock()
            response = await server_module.health_handler(mock_request)

            assert response.status_code == 503
            import json
            body = json.loads(response.body)
            assert body["status"] == "degraded"
            assert body["fortiedr_connected"] is False
