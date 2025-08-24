#!/usr/bin/env python3

import os
import pytest

from meraki_mcp.services.meraki_client import MerakiClient
from meraki_mcp.settings import ApiSettings


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("MERAKI_API_KEY"), reason="MERAKI_API_KEY not set; skipping integration test"
)
def test_meraki_connection():
    """Integration: verifies basic Meraki API connectivity.

    Requires MERAKI_API_KEY to be present in the environment and network access.
    """
    env = ApiSettings()
    client = MerakiClient(api_key=env.MERAKI_API_KEY)
    dashboard = client.get_dashboard()

    organizations = dashboard.organizations.getOrganizations()
    assert isinstance(organizations, list)

    # Basic shape assertion (id/name keys are typical)
    if organizations:
        assert "id" in organizations[0] and "name" in organizations[0]

if __name__ == "__main__":
    # Allow running directly for local verification
    if os.getenv("MERAKI_API_KEY"):
        test_meraki_connection()
    else:
        print("MERAKI_API_KEY not set; skipping local run.")
