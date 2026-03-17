# mcp-fortiedr

A **production-ready FastMCP server** that wraps the complete Fortinet FortiEDR REST API.

Deploy one Docker container per FortiEDR instance (one per customer/tenant). Each container
points at a single FortiEDR host via environment variables.

---

## Architecture

```
┌──────────────────────────┐     ┌──────────────────────────┐
│     MCP Client           │     │     MCP Client           │
└────────────┬─────────────┘     └────────────┬─────────────┘
             │ MCP (streamable-http)           │ MCP
             ▼                                 ▼
┌──────────────────────────┐     ┌──────────────────────────┐
│  mcp-fortiedr-clienteA   │     │  mcp-fortiedr-clienteB   │
│  port 8002               │     │  port 8003               │
│  FORTIEDR_HOST=A         │     │  FORTIEDR_HOST=B         │
└────────────┬─────────────┘     └────────────┬─────────────┘
             │ HTTPS / Basic Auth              │
             ▼                                 ▼
┌──────────────────────────┐     ┌──────────────────────────┐
│  FortiEDR Central        │     │  FortiEDR Central        │
│  Manager – Cliente A     │     │  Manager – Cliente B     │
└──────────────────────────┘     └──────────────────────────┘
```

---

## Quick Start

### 1. Build the image

```bash
cd mcp-fortiedr
docker build -t mcp-fortiedr:latest .
```

### 2. Configure an instance

```bash
cp env.example .env.clienteA
# Edit .env.clienteA with the customer's FortiEDR credentials
```

```env
FORTIEDR_HOST=fortiedr.cliente-a.com
FORTIEDR_USER=api_user
FORTIEDR_PASSWORD=SuperSecret123
FORTIEDR_PORT=443
FORTIEDR_VERIFY_SSL=false
MCP_SERVER_PORT=8000
LOG_LEVEL=INFO
```

### 3. Run a container

```bash
docker run -d \
  --name mcp-fortiedr-clienteA \
  --env-file .env.clienteA \
  -p 8002:8000 \
  mcp-fortiedr:latest
```

### 4. Verify health

```bash
curl http://localhost:8002/health
# {"status":"ok","host":"fortiedr.cliente-a.com","port":443,"fortiedr_connected":true}
```

---

## Adding a New Customer (Step-by-Step)

1. **Create a new env file:**
   ```bash
   cp env.example .env.clienteC
   # Fill in FORTIEDR_HOST, FORTIEDR_USER, FORTIEDR_PASSWORD
   ```

2. **Add a service in docker-compose.yml:**
   ```yaml
   mcp-fortiedr-clienteC:
     image: mcp-fortiedr:latest
     env_file: .env.clienteC
     ports:
       - "8004:8000"
     restart: unless-stopped
   ```

3. **Start the new container:**
   ```bash
   docker-compose up -d mcp-fortiedr-clienteC
   ```

4. **Apunta tu cliente MCP a `http://localhost:8004/`.**

---

## Multi-instance with docker-compose

```bash
# Edit docker-compose.yml and create .env.clienteA, .env.clienteB
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f mcp-fortiedr-clienteA
```

---

## Local Development

```bash
# Install dependencies
pip install -e ".[dev]"
# or
pip install -r requirements.txt

# Set environment
cp env.example .env
# Edit .env

# Run server
PYTHONPATH=src python -m fortiedr_mcp.server

# Run tests (no FortiEDR required – all mocked)
pytest tests/ -v
```

---

## MCP Client Integration

Compatible with any MCP client that supports `streamable-http` transport.

Example configuration (format varies by client):

```json
{
  "mcpServers": {
    "fortiedr-clienteA": {
      "url": "http://localhost:8002/mcp",
      "transport": "http"
    },
    "fortiedr-clienteB": {
      "url": "http://localhost:8003/mcp",
      "transport": "http"
    }
  }
}
```

Example query:
> *"Using fortiedr-clienteA, list all unhandled critical events from the last 24 hours"*

---

## Example: curl

```bash
# List events via MCP (raw tool call)
curl -X POST http://localhost:8002/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "events_list_events",
      "arguments": {
        "organization": "Acme Corp",
        "severities": "Critical,High",
        "handled": false,
        "items_per_page": 10
      }
    }
  }'
```

---

## Available Tools (103 total)

### admin (6 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `admin_list_collector_installers` | GET | List available collector installer packages |
| `admin_list_system_summary` | GET | Get system health and status summary |
| `admin_ready` | GET | System liveness/readiness check |
| `admin_set_system_mode` | PUT | Switch to Simulation or Prevention mode |
| `admin_update_collector_installer` | POST | Schedule collector version upgrade |
| `admin_upload_license` | PUT | Upload a new FortiEDR license |

### audit (1 tool)
| Tool | Method | Description |
|------|--------|-------------|
| `audit_get_audit` | GET | Retrieve audit log entries by date range |

### comm_control (8 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `comm_control_assign_collector_group` | PUT | Assign collector groups to a comm policy |
| `comm_control_clone_policy` | POST | Clone a communication control policy |
| `comm_control_list_policies` | GET | List communication control policies |
| `comm_control_list_products` | GET | List communicating applications |
| `comm_control_resolve_applications` | PUT | Mark applications as resolved/unresolved |
| `comm_control_set_policy_mode` | PUT | Set policy to Simulation/Prevention |
| `comm_control_set_policy_permission` | PUT | Set Allow/Deny for applications in a policy |
| `comm_control_set_policy_rule_state` | PUT | Enable/disable a rule in a policy |

### events (7 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `events_list_events` | GET | List security events with rich filtering |
| `events_count_events` | GET | Count events matching filter criteria |
| `events_create_exception` | POST | Create an exception from an event |
| `events_list_raw_data_items` | GET | List raw telemetry for an event |
| `events_export_raw_data_items_json` | GET | Export raw event data as JSON |
| `events_update_events` | PUT | Mark handled/archived/muted, set classification |
| `events_delete_events` | DELETE | Delete events matching filter |

### exceptions (4 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `exceptions_list_exceptions` | GET | List detection exceptions |
| `exceptions_get_event_exceptions` | GET | Get exceptions for a specific event |
| `exceptions_create_or_edit_exception` | POST | Create or update an exception |
| `exceptions_delete` | DELETE | Delete exceptions matching criteria |

### forensics (3 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `forensics_get_event_file` | GET | Retrieve file/memory from an event |
| `forensics_get_file` | GET | Retrieve a file from a live device |
| `forensics_remediate_device` | PUT | Kill process / delete file / clean persistence |

### hash (1 tool)
| Tool | Method | Description |
|------|--------|-------------|
| `hash_search` | GET | Search file hashes across events and threat-hunting |

### integrations (5 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `integrations_list_connectors` | GET | List external connectors (SIEM, SOAR) |
| `integrations_connectors_metadata` | GET | Get connector schema/metadata |
| `integrations_create_connector` | POST | Create a new connector |
| `integrations_update_connector` | PUT | Update an existing connector |
| `integrations_delete_connector` | DELETE | Delete a connector |
| `integrations_test_connector` | GET | Test connector connectivity |

### inventory (14 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `inventory_list_collectors` | GET | List collector agents |
| `inventory_list_collector_groups` | GET | List collector groups |
| `inventory_create_collector_group` | POST | Create a collector group |
| `inventory_move_collectors` | PUT | Move collectors to a different group |
| `inventory_toggle_collectors` | PUT | Enable or disable collectors |
| `inventory_isolate_collectors` | PUT | Network-isolate devices |
| `inventory_unisolate_collectors` | PUT | Remove network isolation |
| `inventory_delete_collectors` | DELETE | Delete collector records |
| `inventory_list_cores` | GET | List FortiEDR core components |
| `inventory_list_aggregators` | GET | List aggregator components |
| `inventory_list_repositories` | GET | List repository (EDR) components |
| `inventory_list_unmanaged_devices` | GET | List devices without a collector |
| `inventory_system_logs` | GET | Download system diagnostic logs |
| `inventory_collector_logs` | GET | Download collector agent logs |
| `inventory_core_logs` | GET | Download core component logs |
| `inventory_aggregator_logs` | GET | Download aggregator logs |

### iot (7 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `iot_list_iot_devices` | GET | List IoT devices |
| `iot_list_iot_groups` | GET | List IoT groups |
| `iot_create_iot_group` | POST | Create an IoT group |
| `iot_move_iot_devices` | PUT | Move IoT devices to a group |
| `iot_export_iot_json` | GET | Export IoT device data as JSON |
| `iot_rescan_iot_device_details` | PUT | Trigger IoT device rescan |
| `iot_delete_devices` | DELETE | Delete IoT device records |

### ip_sets (4 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `ip_sets_list` | GET | List named IP sets |
| `ip_sets_create` | POST | Create a new IP set |
| `ip_sets_update` | PUT | Update an IP set |
| `ip_sets_delete` | DELETE | Delete IP sets |

### organizations (7 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `organizations_list` | GET | List all organizations |
| `organizations_create` | POST | Create a new organization |
| `organizations_update` | PUT | Update organization settings |
| `organizations_delete` | DELETE | Delete an organization |
| `organizations_export` | GET | Export organization configuration |
| `organizations_transfer_collectors` | POST | Transfer collectors between orgs |
| `organizations_transfer_collectors_stop` | POST | Stop a collector transfer |

### playbooks_policies (6 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `playbooks_list_policies` | GET | List playbook policies |
| `playbooks_clone_policy` | POST | Clone a playbook policy |
| `playbooks_assign_collector_group` | PUT | Assign collector groups to playbook |
| `playbooks_set_mode` | PUT | Set playbook policy mode |
| `playbooks_map_connectors_to_actions` | PUT | Map connectors to actions |
| `playbooks_set_action_classification` | PUT | Set classification mappings |

### policies (6 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `policies_list` | GET | List detection policies |
| `policies_clone` | POST | Clone a detection policy |
| `policies_assign_collector_group` | PUT | Assign collector group to policy |
| `policies_set_mode` | PUT | Set Simulation/Prevention mode |
| `policies_set_rule_state` | PUT | Enable/disable a detection rule |
| `policies_set_rule_action` | PUT | Set action for a detection rule |

### sendable_entities (1 tool)
| Tool | Method | Description |
|------|--------|-------------|
| `sendable_entities_set_mail_format` | PUT | Set alert email format (Text/HTML) |

### system_events (1 tool)
| Tool | Method | Description |
|------|--------|-------------|
| `system_events_list` | GET | List platform health events |

### threat_hunting (11 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `threat_hunting_search` | POST | Search telemetry repository |
| `threat_hunting_counts` | POST | Count threat-hunting results |
| `threat_hunting_facets` | POST | Aggregate telemetry field values |
| `threat_hunting_list_saved_queries` | GET | List saved queries |
| `threat_hunting_save_query` | POST | Save or update a query |
| `threat_hunting_delete_saved_queries` | DELETE | Delete saved queries |
| `threat_hunting_set_query_state` | PUT | Enable/disable saved queries |
| `threat_hunting_customize_fortinet_query` | POST | Customize a Fortinet built-in query |
| `threat_hunting_list_tags` | GET | List query tags |
| `threat_hunting_create_or_edit_tag` | POST | Create or rename a tag |
| `threat_hunting_delete_tags` | DELETE | Delete tags |

### threat_hunting_exclusions (9 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `th_exclusions_list_exclusion_lists` | GET | List exclusion lists |
| `th_exclusions_create_exclusion_list` | POST | Create an exclusion list |
| `th_exclusions_update_exclusion_list` | PUT | Update an exclusion list |
| `th_exclusions_delete_exclusion_list` | DELETE | Delete an exclusion list |
| `th_exclusions_add_exclusions` | POST | Add exclusion entries |
| `th_exclusions_update_exclusions` | PUT | Update exclusion entries |
| `th_exclusions_delete_exclusions` | DELETE | Delete exclusion entries |
| `th_exclusions_get_metadata` | GET | Get exclusion schema metadata |
| `th_exclusions_search` | GET | Search exclusion entries |

### threat_hunting_settings (6 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `th_settings_get_metadata` | GET | Get threat-hunting settings metadata |
| `th_settings_list_profiles` | GET | List collection profiles |
| `th_settings_create_or_update_profile` | POST | Create or update a profile |
| `th_settings_delete_profile` | DELETE | Delete a profile |
| `th_settings_assign_collector_groups_to_profile` | POST | Assign groups to profile |
| `th_settings_clone_profile` | POST | Clone a profile |

### users (7 tools)
| Tool | Method | Description |
|------|--------|-------------|
| `users_list` | GET | List user accounts |
| `users_create` | POST | Create a user |
| `users_update` | PUT | Update a user |
| `users_delete` | DELETE | Delete a user |
| `users_reset_password` | PUT | Reset a user's password |
| `users_get_sp_metadata` | GET | Get SAML SP metadata |
| `users_delete_saml_settings` | DELETE | Delete SAML/SSO settings |

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FORTIEDR_HOST` | ✅ | — | FortiEDR Central Manager hostname or IP |
| `FORTIEDR_USER` | ✅ | — | API username |
| `FORTIEDR_PASSWORD` | ✅ | — | API password |
| `FORTIEDR_PORT` | | `443` | HTTPS port |
| `FORTIEDR_VERIFY_SSL` | | `false` | Verify SSL certificate |
| `MCP_SERVER_PORT` | | `8000` | Port inside the container |
| `LOG_LEVEL` | | `INFO` | Logging level |

---

## Project Structure

```
mcp-fortiedr/
├── src/
│   └── fortiedr_mcp/
│       ├── __init__.py
│       ├── server.py           ← FastMCP entry point + /health endpoint
│       ├── api/
│       │   └── client.py       ← Async aiohttp client (Basic Auth, one host)
│       ├── tools/
│       │   ├── __init__.py     ← register_all() aggregator
│       │   ├── admin.py
│       │   ├── audit.py
│       │   ├── comm_control.py
│       │   ├── events.py
│       │   ├── exceptions.py
│       │   ├── forensics.py
│       │   ├── hash.py
│       │   ├── integrations.py
│       │   ├── inventory.py
│       │   ├── iot.py
│       │   ├── ip_sets.py
│       │   ├── organizations.py
│       │   ├── playbooks_policies.py
│       │   ├── policies.py
│       │   ├── sendable_entities.py
│       │   ├── system_events.py
│       │   ├── threat_hunting.py
│       │   ├── threat_hunting_exclusions.py
│       │   ├── threat_hunting_settings.py
│       │   └── users.py
│       └── utils/
│           └── config.py       ← pydantic-settings configuration
├── tests/
│   └── test_tools.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── env.example
└── README.md
```

---

## Security Notes

- All credentials live **only in environment variables / .env files** – never in code
- The container runs as a **non-root user** (`appuser`)
- SSL verification is **configurable** per instance (`FORTIEDR_VERIFY_SSL`)
- Sensitive `.env.*` files should be **excluded from version control** (add to `.gitignore`)
