import json
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from meraki_mcp.services.meraki_client import MerakiClient
from meraki_mcp.settings import ApiSettings

logger = logging.getLogger(__name__)

env = ApiSettings()


class CommonlyUsedMerakiApiTools:
    """
    Provides direct MCP tools for commonly used Meraki API endpoints.

    These tools offer faster access to frequently used API calls without
    requiring the search and discovery process.
    """

    def __init__(self, mcp: FastMCP, meraki_client: MerakiClient, enabled: bool):
        self.mcp = mcp
        self.meraki_client = meraki_client
        self.dashboard = self.meraki_client.get_dashboard()
        self.enabled = enabled
        if self.enabled:
            self._register_tools()
        else:
            logger.info("RegularApiTools not registered (MERAKI_API_KEY not set)")

    def _register_tools(self):
        """Register all regular API tools with the MCP server."""

        @self.mcp.tool()
        def get_organizations() -> str:
            """
            Get all organizations accessible by the API key.

            This is one of the most commonly used endpoints to discover available
            organizations before making other API calls.

            Returns:
                JSON string containing list of organizations with their details
                including organizationId, name, url, and other metadata.
            """
            try:
                organizations = self.dashboard.organizations.getOrganizations()

                result = {
                    "method": "getOrganizations",
                    "count": len(organizations),
                    "organizations": organizations,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get organizations: {e}")
                return json.dumps(
                    {"error": "API call failed", "message": str(e)}, indent=2
                )

        @self.mcp.tool()
        def get_organization_devices(organization_id: str) -> str:
            """
            Get all devices in an organization.

            This is commonly used to discover available devices across all networks
            in an organization for inventory and management purposes.

            Args:
                organization_id: The organization identifier (e.g., "123456")

            Returns:
                JSON string containing list of all devices in the organization
                with details like serial, model, name, networkId, etc.
            """
            try:
                devices = self.dashboard.organizations.getOrganizationDevices(
                    organizationId=organization_id
                )

                result = {
                    "method": "getOrganizationDevices",
                    "organization_id": organization_id,
                    "count": len(devices),
                    "devices": devices,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get organization devices: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "organization_id": organization_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_organization_networks(organization_id: str) -> str:
            """
            Get all networks in an organization.

            Essential for discovering available networks before making
            network-specific API calls.

            Args:
                organization_id: The organization identifier (e.g., "123456")

            Returns:
                JSON string containing list of networks with networkId, name,
                productTypes, timezone, and other network metadata.
            """
            try:
                networks = self.dashboard.organizations.getOrganizationNetworks(
                    organizationId=organization_id
                )

                result = {
                    "method": "getOrganizationNetworks",
                    "organization_id": organization_id,
                    "count": len(networks),
                    "networks": networks,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get organization networks: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "organization_id": organization_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_device_status(serial: str) -> str:
            """
            Get device status and basic information.

            Frequently used to check device health, connectivity, and
            basic configuration details.

            Args:
                serial: Device serial number (e.g., "Q2XX-XXXX-XXXX")

            Returns:
                JSON string containing device information including status,
                model, name, networkId, lan/wan IP addresses, and other details.
            """
            try:
                device = self.dashboard.devices.getDevice(serial=serial)

                result = {"method": "getDevice", "serial": serial, "device": device}

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get device status: {e}")
                return json.dumps(
                    {"error": "API call failed", "message": str(e), "serial": serial},
                    indent=2,
                )

        @self.mcp.tool()
        def get_network_clients(
            network_id: str, timespan: Optional[int] = 2592000
        ) -> str:
            """
            Get clients connected to a network.

            Commonly used for monitoring connected devices and user activity.
            Default timespan is 30 days (2592000 seconds).

            Args:
                network_id: The network identifier (e.g., "N_12345")
                timespan: Time range in seconds (max 2592000 = 30 days)

            Returns:
                JSON string containing list of network clients with MAC addresses,
                IP assignments, device types, usage statistics, etc.
            """
            try:
                clients = self.dashboard.networks.getNetworkClients(
                    networkId=network_id, timespan=timespan
                )

                result = {
                    "method": "getNetworkClients",
                    "network_id": network_id,
                    "timespan": timespan,
                    "count": len(clients),
                    "clients": clients,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get network clients: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "network_id": network_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_switch_port_config(serial: str, port_id: str) -> str:
            """
            Get switch port configuration.

            Frequently used for troubleshooting port settings, VLAN assignments,
            and access control configurations.

            Args:
                serial: Switch serial number (e.g., "Q2XX-XXXX-XXXX")
                port_id: Port identifier (e.g., "1", "2", "24")

            Returns:
                JSON string containing port configuration including VLAN settings,
                access policy, power settings, and other port-specific details.
            """
            try:
                port_config = self.dashboard.switch.getDeviceSwitchPort(
                    serial=serial, portId=port_id
                )

                result = {
                    "method": "getDeviceSwitchPort",
                    "serial": serial,
                    "port_id": port_id,
                    "configuration": port_config,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get switch port config: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "serial": serial,
                        "port_id": port_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_network_settings(network_id: str) -> str:
            """
            Get network configuration settings.

            Used to review network-wide settings including local status page,
            remote status page, and other network preferences.

            Args:
                network_id: The network identifier (e.g., "N_12345")

            Returns:
                JSON string containing network settings and configuration details.
            """
            try:
                settings = self.dashboard.networks.getNetworkSettings(
                    networkId=network_id
                )

                result = {
                    "method": "getNetworkSettings",
                    "network_id": network_id,
                    "settings": settings,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get network settings: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "network_id": network_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_firewall_rules(network_id: str) -> str:
            """
            Get Layer 3 firewall rules for a network.

            Commonly used for security auditing and firewall policy management.

            Args:
                network_id: The network identifier (e.g., "N_12345")

            Returns:
                JSON string containing firewall rules with policies, protocols,
                source/destination addresses, and rule priorities.
            """
            try:
                firewall_rules = (
                    self.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(
                        networkId=network_id
                    )
                )

                result = {
                    "method": "getNetworkApplianceFirewallL3FirewallRules",
                    "network_id": network_id,
                    "rules": firewall_rules,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get firewall rules: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "network_id": network_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_organization_uplinks_statuses(organization_id: str) -> str:
            """
            Get uplink status for all devices in an organization.

            Essential for monitoring network connectivity and identifying
            connectivity issues across the organization.

            Args:
                organization_id: The organization identifier (e.g., "123456")

            Returns:
                JSON string containing uplink status for all organization devices
                including interface information, IP addresses, and connectivity status.
            """
            try:
                uplinks = self.dashboard.organizations.getOrganizationUplinksStatuses(
                    organizationId=organization_id
                )

                result = {
                    "method": "getOrganizationUplinksStatuses",
                    "organization_id": organization_id,
                    "count": len(uplinks),
                    "uplinks": uplinks,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get organization uplinks: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "organization_id": organization_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_network_topology(network_id: str) -> str:
            """
            Get network topology including device relationships and connections.

            Useful for understanding network architecture and device connectivity.

            Args:
                network_id: The network identifier (e.g., "N_12345")

            Returns:
                JSON string containing network topology with device links and connections.
            """
            try:
                topology = self.dashboard.networks.getNetworkTopologyLinkLayer(
                    networkId=network_id
                )

                result = {
                    "method": "getNetworkTopologyLinkLayer",
                    "network_id": network_id,
                    "topology": topology,
                }

                return json.dumps(result, indent=2)

            except Exception as e:
                logger.error(f"Failed to get network topology: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "network_id": network_id,
                    },
                    indent=2,
                )

        # Administered identity and API keys wrappers (OAuth-compatible endpoints)

        @self.mcp.tool()
        def administered_get_identity() -> str:
            """
            Returns the identity of the current user.

            Calls: GET /administered/identities/me
            """
            try:
                identity = self.dashboard.administered.getAdministeredIdentitiesMe()
                return json.dumps(
                    {"method": "getAdministeredIdentitiesMe", "identity": identity},
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to get administered identity: {e}")
                return json.dumps({"error": "API call failed", "message": str(e)}, indent=2)

        @self.mcp.tool()
        def administered_list_api_keys() -> str:
            """
            List non-sensitive metadata for API keys belonging to the current user.

            Calls: GET /administered/identities/me/api/keys
            """
            try:
                keys = self.dashboard.administered.getAdministeredIdentitiesMeApiKeys()
                return json.dumps(
                    {"method": "getAdministeredIdentitiesMeApiKeys", "keys": keys},
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to list administered API keys: {e}")
                return json.dumps({"error": "API call failed", "message": str(e)}, indent=2)

        @self.mcp.tool()
        def administered_generate_api_key() -> str:
            """
            Generate a new API key for the current user.

            Calls: POST /administered/identities/me/api/keys/generate
            """
            try:
                response = self.dashboard.administered.generateAdministeredIdentitiesMeApiKeys()
                return json.dumps(
                    {
                        "method": "generateAdministeredIdentitiesMeApiKeys",
                        "response": response,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to generate administered API key: {e}")
                return json.dumps({"error": "API call failed", "message": str(e)}, indent=2)

        @self.mcp.tool()
        def administered_revoke_api_key(suffix: str) -> str:
            """
            Revoke an API key by its last four characters.

            Args:
                suffix: Last four characters of the API key to revoke.

            Calls: POST /administered/identities/me/api/keys/{suffix}/revoke
            """
            try:
                response = self.dashboard.administered.revokeAdministeredIdentitiesMeApiKeys(
                    suffix=suffix
                )
                return json.dumps(
                    {
                        "method": "revokeAdministeredIdentitiesMeApiKeys",
                        "suffix": suffix,
                        "response": response,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to revoke administered API key: {e}")
                return json.dumps(
                    {"error": "API call failed", "message": str(e), "suffix": suffix},
                    indent=2,
                )

        # Spaces and Sensor Gateway convenience wrappers

        @self.mcp.tool()
        def get_spaces_integration_status(organization_id: str) -> str:
            """
            Get the status of the Spaces integration in Meraki for an organization.

            Calls: GET /organizations/{organizationId}/spaces/integrate/status
            """
            try:
                if not hasattr(
                    self.dashboard.organizations,
                    "getOrganizationSpacesIntegrateStatus",
                ):
                    return json.dumps(
                        {
                            "error": "method_unavailable_in_sdk",
                            "message": "getOrganizationSpacesIntegrateStatus is not available in the installed meraki SDK",
                            "sdk_version_hint": "Upgrade the 'meraki' Python package to a version supporting Spaces",
                            "organization_id": organization_id,
                        },
                        indent=2,
                    )
                status = self.dashboard.organizations.getOrganizationSpacesIntegrateStatus(
                    organizationId=organization_id
                )
                return json.dumps(
                    {
                        "method": "getOrganizationSpacesIntegrateStatus",
                        "organization_id": organization_id,
                        "status": status,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to get Spaces integration status: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "organization_id": organization_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def get_sensor_gateway_latest_connections(organization_id: str) -> str:
            """
            Returns latest sensor-gateway connectivity data for an organization.

            Calls: GET /organizations/{organizationId}/sensor/gateways/connections/latest
            """
            try:
                if not hasattr(
                    self.dashboard.sensor,
                    "getOrganizationSensorGatewaysConnectionsLatest",
                ):
                    return json.dumps(
                        {
                            "error": "method_unavailable_in_sdk",
                            "message": "getOrganizationSensorGatewaysConnectionsLatest is not available in the installed meraki SDK",
                            "sdk_version_hint": "Upgrade the 'meraki' Python package to a version supporting Sensor Gateway latest connections",
                            "organization_id": organization_id,
                        },
                        indent=2,
                    )
                latest = (
                    self.dashboard.sensor.getOrganizationSensorGatewaysConnectionsLatest(
                        organizationId=organization_id
                    )
                )
                return json.dumps(
                    {
                        "method": "getOrganizationSensorGatewaysConnectionsLatest",
                        "organization_id": organization_id,
                        "data": latest,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(
                    f"Failed to get sensor gateway latest connections: {e}"
                )
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "organization_id": organization_id,
                    },
                    indent=2,
                )

        # XDR enable/disable and Wireless scanning/L7 firewall wrappers

        @self.mcp.tool()
        def enable_xdr_on_networks(organization_id: str, network_ids_json: str) -> str:
            """
            Enable XDR on specified networks in an organization.

            Args:
                organization_id: Organization ID
                network_ids_json: JSON array of network IDs, e.g. '["N_1","N_2"]'
            """
            try:
                network_ids = json.loads(network_ids_json) if network_ids_json else []
                response = self.dashboard.organizations.enableOrganizationIntegrationsXdrNetworks(
                    organizationId=organization_id, networkIds=network_ids
                )
                return json.dumps(
                    {
                        "method": "enableOrganizationIntegrationsXdrNetworks",
                        "organization_id": organization_id,
                        "network_ids": network_ids,
                        "response": response,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to enable XDR: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "organization_id": organization_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def disable_xdr_on_networks(organization_id: str, network_ids_json: str) -> str:
            """
            Disable XDR on specified networks in an organization.
            """
            try:
                network_ids = json.loads(network_ids_json) if network_ids_json else []
                response = self.dashboard.organizations.disableOrganizationIntegrationsXdrNetworks(
                    organizationId=organization_id, networkIds=network_ids
                )
                return json.dumps(
                    {
                        "method": "disableOrganizationIntegrationsXdrNetworks",
                        "organization_id": organization_id,
                        "network_ids": network_ids,
                        "response": response,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to disable XDR: {e}")
                return json.dumps(
                    {
                        "error": "API call failed",
                        "message": str(e),
                        "organization_id": organization_id,
                    },
                    indent=2,
                )

        @self.mcp.tool()
        def update_network_wireless_scanning_settings(network_id: str, settings_json: str) -> str:
            """
            Change scanning API settings for a network.

            Args:
                network_id: Network ID
                settings_json: JSON object body per API
            """
            try:
                settings = json.loads(settings_json) if settings_json else {}
                response = self.dashboard.wireless.updateNetworkWirelessLocationScanning(
                    networkId=network_id, **settings
                )
                return json.dumps(
                    {
                        "method": "updateNetworkWirelessLocationScanning",
                        "network_id": network_id,
                        "request": settings,
                        "response": response,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to update wireless scanning settings: {e}")
                return json.dumps(
                    {"error": "API call failed", "message": str(e), "network_id": network_id},
                    indent=2,
                )

        @self.mcp.tool()
        def update_ssid_l7_firewall_rules(network_id: str, number: int, rules_json: str) -> str:
            """
            Update the L7 firewall rules of an SSID on an MR network.

            Args:
                network_id: Network ID
                number: SSID number
                rules_json: JSON body per API
            """
            try:
                rules = json.loads(rules_json) if rules_json else {}
                if not hasattr(
                    self.dashboard.wireless,
                    "updateNetworkWirelessSsidFirewallL7FirewallRules",
                ):
                    return json.dumps(
                        {
                            "error": "method_unavailable_in_sdk",
                            "message": "updateNetworkWirelessSsidFirewallL7FirewallRules is not available in the installed meraki SDK",
                            "sdk_version_hint": "Upgrade the 'meraki' Python package or use dynamic executor",
                            "network_id": network_id,
                            "number": number,
                        },
                        indent=2,
                    )
                response = self.dashboard.wireless.updateNetworkWirelessSsidFirewallL7FirewallRules(
                    networkId=network_id, number=number, **rules
                )
                return json.dumps(
                    {
                        "method": "updateNetworkWirelessSsidFirewallL7FirewallRules",
                        "network_id": network_id,
                        "number": number,
                        "request": rules,
                        "response": response,
                    },
                    indent=2,
                )
            except Exception as e:
                logger.error(f"Failed to update SSID L7 firewall rules: {e}")
                return json.dumps(
                    {"error": "API call failed", "message": str(e), "network_id": network_id, "number": number},
                    indent=2,
                )
