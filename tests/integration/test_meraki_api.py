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
    env = ApiSettings()
    client = MerakiClient(api_key=env.MERAKI_API_KEY)
    dashboard = client.get_dashboard()
    organizations = dashboard.organizations.getOrganizations()
    assert isinstance(organizations, list)
    if organizations:
        assert "id" in organizations[0] and "name" in organizations[0]

