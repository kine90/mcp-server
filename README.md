# Meraki MCP

[![CI](https://github.com/merakimiles/mcp-server/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/merakimiles/mcp-server/actions/workflows/ci.yml)

A powerful Model Context Protocol (MCP) server that provides dynamic access to the entire Meraki Dashboard API plus advanced compliance and security auditing capabilities. Instead of creating hundreds of individual tools, Meraki MCP uses intelligent discovery to find and execute any Meraki API endpoint on demand.

## 🚀 Features

### **Dynamic API Discovery**

- **Universal Access**: Query any of 400+ Meraki API endpoints without pre-defined tools
- **Single-Call Optimization**: Common queries (organizations, device status, etc.) found instantly
- **Intelligent Search**: Natural language queries to find relevant endpoints
- **Parameter Discovery**: Automatic detection of required and optional parameters
- **Smart Validation**: Generic parameter validation with helpful error messages

### **Compliance & Security Auditing** 🛡️

- **Multi-Framework Support**: PCI DSS, HIPAA, SOC2, ISO 27001, NIST Cybersecurity Framework
- **Automated Compliance Scanning**: Comprehensive security assessments across your entire Meraki organization
- **Critical Finding Detection**: Identifies security gaps and compliance violations
- **Actionable Recommendations**: Specific remediation steps for each finding
- **Detailed Reporting**: Executive summaries and technical details for compliance documentation

### **Backup & Restore Operations** 🔄

- **Organization Backup**: Create complete backups of your Meraki organization
- **Component Restore**: Restore individual devices or networks from backups
- **Status Monitoring**: Real-time progress tracking for backup and restore operations
- **Error Handling**: Comprehensive error reporting and recovery guidance

### **Advanced Network Analysis** 📊

- **Network Topology Analysis**: Comprehensive device relationships and connections
- **Device Health Monitoring**: Performance metrics and diagnostics
- **Security Auditing**: Network-wide security assessments
- **Performance Analytics**: Bottleneck identification and optimization recommendations
- **Configuration Drift Detection**: Identify inconsistencies across networks

> Acknowledgement: This project was originally inspired by earlier work that included Selent-specific features. Those integrations have been removed; thanks to the Selent team for prior inspiration.

## 🎯 Setup for Cursor IDE (with Secure Keychain Storage)

This section explains how to securely configure the Meraki MCP server in Cursor IDE using macOS Keychain for API key storage.

### Prerequisites

- Cursor IDE installed
- Docker installed and running
- macOS (for Keychain support)
- A Meraki Dashboard API key

### Secure Setup Steps

#### 1. Store API Key in macOS Keychain

Use the provided setup script to securely store your API key:

```bash
chmod +x setup_meraki_api_key.sh
./setup_meraki_api_key.sh
```

This script will:
- Prompt you for your Meraki API key (input is hidden)
- Store it securely in macOS Keychain
- Provide instructions for exporting it to your shell

Alternatively, store it manually:

```bash
security add-generic-password \
    -a "meraki-mcp" \
    -s "MERAKI_API_KEY" \
    -w "your_actual_api_key_here" \
    -U
```

#### 2. Build the Docker Image

Build the Docker image from source:

```bash
docker build -t meraki-mcp:latest .
```

#### 3. Configure Cursor MCP

Create the MCP configuration file at `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "Meraki MCP": {
      "command": "/absolute/path/to/repo/meraki-mcp-docker.sh",
      "args": []
    }
  }
}
```

**Important:** Replace `/absolute/path/to/repo/` with the actual path to your cloned repository.

The `meraki-mcp-docker.sh` wrapper script will:
- Retrieve your API key from Keychain
- Pass it securely to the Docker container
- Start the MCP server with proper configuration

#### 4. Set Up Shell Environment (Optional)

For terminal usage, add this to your `~/.zshrc` (or `~/.bash_profile`):

```bash
# Load Meraki API Key from Keychain
export MERAKI_API_KEY=$(security find-generic-password -a "meraki-mcp" -s "MERAKI_API_KEY" -w 2>/dev/null)
```

Then reload your shell:

```bash
source ~/.zshrc
```

#### 5. Restart Cursor

1. Quit Cursor completely (Cmd+Q)
2. Reopen Cursor
3. Go to Settings → Tools & MCP
4. Verify "Meraki MCP" appears under "Installed MCP Servers"

### Security Benefits

✅ **No Hardcoded Keys**: API keys are never stored in configuration files  
✅ **Keychain Encryption**: Keys are encrypted by macOS Keychain  
✅ **Automatic Retrieval**: Wrapper script retrieves keys securely at runtime  
✅ **No Version Control Risk**: Keys are excluded from git repositories  
✅ **Easy Rotation**: Update keys in Keychain without changing config files  

### Troubleshooting

**Container exits immediately:**
- Verify the Docker image is built: `docker images | grep meraki-mcp`
- Check wrapper script is executable: `chmod +x meraki-mcp-docker.sh`
- Test manually: `./meraki-mcp-docker.sh`

**API key not found:**
- Verify key exists: `security find-generic-password -a "meraki-mcp" -s "MERAKI_API_KEY"`
- Re-run setup script if needed

**Cursor doesn't see MCP server:**
- Verify config file location: `~/.cursor/mcp.json`
- Check file permissions: `chmod 600 ~/.cursor/mcp.json`
- Ensure absolute path in config is correct
- Restart Cursor completely

**Multiple containers running:**
- This is normal - Cursor may maintain multiple MCP connections
- Containers auto-stop when Cursor disconnects (due to `--rm` flag)
- To manually stop: `docker stop $(docker ps -q --filter "ancestor=meraki-mcp")`

### Files Created

- `setup_meraki_api_key.sh` - Interactive script to store API key in Keychain
- `get_meraki_api_key.sh` - Helper script to retrieve key from Keychain
- `meraki-mcp-docker.sh` - Wrapper script that retrieves key and runs Docker container
- `~/.cursor/mcp.json` - Cursor MCP configuration file

## 📖 Usage Examples

### **API Operations**

```
# Get device information
"Get device Q4AB-WMAB-TAZU configuration for port number 4"

# List organizations
"Show me all my Meraki organizations"

# Get network clients
"List all clients in network N_12345"

# Firewall rules
"Get MX firewall rules for device Q2KN-Q6GH-CREQ"
```

### **Compliance Testing**

```
# Get available compliance frameworks
"What compliance types are available?"

# Run PCI DSS compliance test
"Run PCI compliance test on my organization"

# Test SOC2 compliance
"Perform SOC2 compliance audit"

# NIST Cybersecurity Framework assessment
"Run NIST compliance check"
```

### **Backup & Restore**

```
# Create organization backup
"Create a backup of my entire Meraki organization"

# Check backup status
"What's the status of backup abc123?"

# Restore a device
"Restore device Q2XX-XXXX-XXXX from backup abc123"

# Restore a network
"Restore network L_123456789 from backup abc123"
```

### **Advanced Analytics**

```
# Network topology analysis
"Analyze the topology of network N_12345"

# Device health check
"Check the health of device Q2XX-XXXX-XXXX"

# Security audit
"Perform security audit on network N_12345"

# Performance analysis
"Analyze performance of network N_12345"
```

## 🛠 Development & Management

### **Container Management**

```bash
# Check status
docker ps --filter name=meraki-mcp-server

# View logs
docker logs -f meraki-mcp-server

# Restart
docker-compose restart

# Stop
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## 🔧 Available Tools

### **Core API Tools**

- `search_meraki_api_endpoints(query)`
  - Natural-language search over the Meraki SDK (e.g., "wireless ssids", "mx firewall rules")
- `get_meraki_endpoint_parameters(section, method)`
  - Introspect required/optional params for any endpoint
- `execute_meraki_api_endpoint(section, method, serial?, portId?, networkId?, organizationId?, kwargs='{}')`
  - Call any Meraki API directly; pass extra params as JSON in `kwargs`

### **Convenience Tools**

- Organizations and networks
  - `get_organizations`, `get_organization_networks(organization_id)`, `get_organization_devices(organization_id)`
- Devices and switch
  - `get_device_status(serial)`, `get_switch_port_config(serial, port_id)`
- Network
  - `get_network_clients(network_id, timespan?)`, `get_network_settings(network_id)`, `get_network_topology(network_id)`
- Security (MX)
  - `get_firewall_rules(network_id)`
- Administered (user/keys)
  - `administered_get_identity()`, `administered_list_api_keys()`, `administered_generate_api_key()`, `administered_revoke_api_key(suffix)`
- Integrations
  - `enable_xdr_on_networks(organization_id, network_ids_json)`, `disable_xdr_on_networks(organization_id, network_ids_json)`
- Wireless
  - `update_network_wireless_scanning_settings(network_id, settings_json)`
  - `update_ssid_l7_firewall_rules(network_id, number, rules_json)`
- Sensor/Spaces (SDK dependent)
  - `get_sensor_gateway_latest_connections(organization_id)`
  - `get_spaces_integration_status(organization_id)`

Tip: You can always fall back to the dynamic trio: search → parameters → execute.

## 💡 Key Benefits

✅ **No Manual Tool Creation**: Access 400+ endpoints without writing individual tools  
✅ **Single-Call Efficiency**: Common queries resolved instantly without multiple searches  
✅ **Intelligent Discovery**: Natural language queries find the right endpoints  
✅ **Always Up-to-Date**: Uses live Meraki API, automatically includes new endpoints  
✅ **Production Ready**: Docker deployment for consistency across environments  
✅ **Multi-User Support**: Scale across teams with individual API keys  
✅ **Performance Optimized**: Caching, error handling, and smart parameter validation  
✅ **Compliance Ready**: Built-in support for PCI DSS, HIPAA, SOC2, ISO 27001, NIST  
✅ **Auto-Updates**: `--pull=always` ensures latest features and security patches  
✅ **Enterprise Features**: Backup/restore, security auditing, performance analytics

## 🔐 Security & Environment

### MCP Security Guidance

This project aligns with the Model Context Protocol Security guidance for building and operating MCP servers. See the MCP Security site for the Top 10 risks, hardening guidance, and operational best practices:

- Model Context Protocol Security: https://modelcontextprotocol-security.io

Key practices we follow and recommend:
- Do not log sensitive data; keep request/response logging minimal and sanitized
- Use environment variables for secrets (e.g., `MERAKI_API_KEY`), never commit secrets
- Prefer read-only operations by default in production; explicitly confirm mutations
- Restrict dynamic surface area (allow/deny lists for sections/methods) when needed
- Run containers as non-root and drop unnecessary capabilities in production

### **Environment Variables**

| Variable              | Required | Description                                                   |
| --------------------- | -------- | ------------------------------------------------------------- |
| `MERAKI_API_KEY`      | Yes      | Your Meraki Dashboard API key                                 |
 

### **Security Best Practices**

- Never commit API keys to version control
- Use environment variables or secure secret management
- **For macOS users**: Use Keychain for secure API key storage (see Cursor setup section above)
- Scan Docker images for vulnerabilities in production
- Set appropriate resource limits for containers
- Use secure networks in production deployments

### **Secure API Key Storage (macOS)**

For Cursor IDE users on macOS, we provide scripts to store API keys securely in macOS Keychain:

- `setup_meraki_api_key.sh` - Stores your API key in Keychain
- `get_meraki_api_key.sh` - Retrieves key from Keychain
- `meraki-mcp-docker.sh` - Wrapper script that uses Keychain-stored keys

This approach ensures:
- Keys are encrypted by macOS Keychain
- No keys in configuration files or environment variables
- Easy key rotation without changing configs
- Protection against accidental exposure

See the [Cursor IDE Setup](#-setup-for-cursor-ide-with-secure-keychain-storage) section for detailed instructions.

---

## 🤝 Contributing

- Start here: see `AGENTS.md` for project structure, commands, style, and testing.
- Use Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).
- Ensure CI passes: `ruff`, `mypy`, and unit `pytest`.
- Integration tests are opt-in: `MERAKI_API_KEY=... pytest -m integration -q`.
- PRs use the template in `.github/pull_request_template.md` and must link issues when applicable.

## 🚧 Roadmap / Improvements

- Security & Hardening
  - Add output redaction middleware for sensitive fields (psk, password, secret, token, apiKey)
  - Safe mode default: block create/update/delete unless `ALLOW_MUTATIONS=true` and `confirm=true`
  - Gate high‑risk tools (e.g., administered_*) behind `ENABLE_ADMINISTERED_TOOLS=true`
  - Allow/Deny lists to restrict dynamic executor surface: `ALLOW_SECTIONS/METHODS`, `DENY_SECTIONS/METHODS`
  - Add rate/size guards (`MAX_PER_PAGE`, `MAX_TIMESPAN`, `MAX_PARALLEL_CALLS`) to prevent resource exhaustion
  - Container hardening: run as non‑root, drop Linux capabilities, consider read‑only FS in production
  - If exposed remotely: enforce TLS, IP allowlists, and gateway authentication

- Coverage & SDK Parity
  - Track OpenAPI v1.61+ additions (Zigbee IoT, Sensor Gateway, Spaces) as wrappers when SDK support lands
  - Expand convenience wrappers (MG eSIM, Insight, SM, Webhooks) while keeping dynamic executor
  - Keep `meraki` SDK current and add CI checks for method presence

- Testing & Quality
  - Unit tests for wrappers and semantic search matching
  - Integration smoke tests (read‑only) with environment‑gated live checks
  - CI pipeline: lint, type‑check, test matrix (local/Docker)

- Observability & Ops
  - Optional sanitized audit logs (tool name, section.method, status, latency)
  - Health/readiness endpoints and structured logs for container platforms

- DX & Distribution
  - Example configs and scripts for local dev and Docker

Reference security guidance: Model Context Protocol Security — Top 10 and Hardening Guide: https://modelcontextprotocol-security.io
