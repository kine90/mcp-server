#!/bin/bash
# Wrapper script to run Meraki MCP Docker container with API key from Keychain
# This script retrieves the API key from macOS Keychain and passes it to Docker

set -e

# Retrieve API key from Keychain
API_KEY=$(security find-generic-password -a "meraki-mcp" -s "MERAKI_API_KEY" -w 2>/dev/null)

if [ -z "$API_KEY" ]; then
    echo "Error: Could not retrieve MERAKI_API_KEY from Keychain" >&2
    echo "Please run: ./setup_meraki_api_key.sh" >&2
    exit 1
fi

# Run Docker with the API key
# Using local image (built from source)
exec docker run \
    -i \
    --rm \
    -e "MERAKI_API_KEY=$API_KEY" \
    meraki-mcp:latest \
    "$@"

