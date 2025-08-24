import asyncio
import json

import pytest

from meraki_mcp.tools.meraki_api_tools import MerakiApiTools
from meraki_mcp.settings import ApiSettings


class DummyDevicesAPI:
    # Class name contains 'API' to satisfy discovery heuristic
    def getDevice(self, serial):  # noqa: N802 (Meraki-style naming)
        return {"serial": serial, "name": "Device X", "apiKey": "SECRET"}

    def updateNetworkName(self, networkId, name, confirm=False):  # noqa: N802
        return {"networkId": networkId, "name": name, "updated": True}


class DummyDashboard:
    def __init__(self):
        self.devices = DummyDevicesAPI()


class FakeMerakiClient:
    def get_dashboard(self):
        return DummyDashboard()


class FakeMCP:
    def tool(self):
        def decorator(fn):
            return fn

        return decorator


def test_get_parameters_discovers_required_signature():
    tools = MerakiApiTools(FakeMCP(), FakeMerakiClient(), enabled=True, settings=ApiSettings())
    # getDevice requires serial
    text = asyncio.run(tools.get_meraki_endpoint_parameters("devices", "getDevice"))
    data = json.loads(text)
    assert data["parameters"]["serial"]["required"] is True


def test_execute_redacts_and_denies_mutations_by_default():
    s = ApiSettings()
    s.ALLOW_MUTATIONS = False
    tools = MerakiApiTools(FakeMCP(), FakeMerakiClient(), enabled=True, settings=s)

    # Non-mutation call works and redacts sensitive keys
    res = asyncio.run(tools.execute_meraki_api_endpoint("devices", "getDevice", serial="Q2XX"))
    data = json.loads(res)
    assert data["serial"] == "Q2XX"
    # apiKey should be redacted
    assert data["apiKey"] == "***REDACTED***"

    # Mutation should be blocked
    denied = asyncio.run(
        tools.execute_meraki_api_endpoint(
            "devices", "updateNetworkName", networkId="N_1", kwargs="{\"name\": \"New\"}"
        )
    )
    d = json.loads(denied)
    assert d.get("error") is not None
    assert "disabled" in d.get("error") or "blocked" in d.get("error")


def test_execute_allows_with_confirm_and_policy():
    s = ApiSettings()
    s.ALLOW_MUTATIONS = True
    s.REQUIRE_CONFIRM_FOR_MUTATIONS = True
    tools = MerakiApiTools(FakeMCP(), FakeMerakiClient(), enabled=True, settings=s)

    ok = asyncio.run(
        tools.execute_meraki_api_endpoint(
            "devices",
            "updateNetworkName",
            networkId="N_1",
            kwargs='{"name": "New", "confirm": true}',
        )
    )
    data = json.loads(ok)
    assert data["updated"] is True


def test_deny_lists_block_execution():
    s = ApiSettings()
    s.DENY_SECTIONS = ["devices"]
    tools = MerakiApiTools(FakeMCP(), FakeMerakiClient(), enabled=True, settings=s)
    res = asyncio.run(tools.execute_meraki_api_endpoint("devices", "getDevice", serial="Q2XX"))
    data = json.loads(res)
    assert data.get("error") == "execution blocked"

