import logging

from mcp.server.fastmcp import FastMCP

from meraki_mcp.services.meraki_client import MerakiClient
from meraki_mcp.settings import ApiSettings
from meraki_mcp.tools.commonly_used_api_tools import CommonlyUsedMerakiApiTools
from meraki_mcp.tools.meraki_api_tools import MerakiApiTools
from meraki_mcp.tools.meraki_complex_api_tools import MerakiComplexApiTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = ApiSettings()
mcp: FastMCP = FastMCP("Meraki MCP")

meraki_client = MerakiClient(api_key=env.MERAKI_API_KEY)

meraki_api_tools = MerakiApiTools(
    mcp, meraki_client, enabled=bool(env.MERAKI_API_KEY), settings=env
)
meraki_complex_api_tools = MerakiComplexApiTools(
    mcp, meraki_client, enabled=bool(env.MERAKI_API_KEY)
)
commonly_used_meraki_api_tools = CommonlyUsedMerakiApiTools(
    mcp, meraki_client, enabled=bool(env.MERAKI_API_KEY)
)


def main():
    # Log Meraki SDK version and available top-level sections for visibility
    try:
        dashboard = meraki_client.get_dashboard()
        try:
            import meraki as _meraki

            logger.info(f"Meraki SDK version: {_meraki.__version__}")
        except Exception:
            pass

        sections = [
            attr
            for attr in dir(dashboard)
            if not attr.startswith("_")
            and hasattr(getattr(dashboard, attr), "__class__")
            and "api" in str(type(getattr(dashboard, attr))).lower()
        ]
        logger.info(f"Meraki API sections discovered: {sorted(sections)[:20]}")
    except Exception as e:
        logger.warning(f"Unable to enumerate Meraki API sections at startup: {e}")
    mcp.run()


if __name__ == "__main__":
    main()
