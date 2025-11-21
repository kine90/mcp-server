#!/bin/bash
# Helper script to retrieve Meraki API Key from Keychain
# Usage: source this file or run: export MERAKI_API_KEY=$(./get_meraki_api_key.sh)

security find-generic-password -a "meraki-mcp" -s "MERAKI_API_KEY" -w 2>/dev/null

