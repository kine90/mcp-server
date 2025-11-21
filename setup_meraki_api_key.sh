#!/bin/bash
# Secure setup script for Meraki API Key
# This script helps you store your API key securely using macOS Keychain

set -e

echo "🔐 Meraki MCP API Key Setup"
echo "============================"
echo ""

# Check if keychain item already exists
if security find-generic-password -a "meraki-mcp" -s "MERAKI_API_KEY" &>/dev/null; then
    echo "⚠️  API key already exists in Keychain."
    read -p "Do you want to update it? (y/N): " update
    if [[ ! "$update" =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    security delete-generic-password -a "meraki-mcp" -s "MERAKI_API_KEY" &>/dev/null || true
fi

# Prompt for API key
read -sp "Enter your Meraki API Key: " api_key
echo ""

if [ -z "$api_key" ]; then
    echo "❌ Error: API key cannot be empty"
    exit 1
fi

# Store in macOS Keychain
security add-generic-password \
    -a "meraki-mcp" \
    -s "MERAKI_API_KEY" \
    -w "$api_key" \
    -U \
    -T "/usr/bin/security" \
    -T "/Applications/Cursor.app/Contents/MacOS/Cursor" 2>/dev/null || \
security add-generic-password \
    -a "meraki-mcp" \
    -s "MERAKI_API_KEY" \
    -w "$api_key" \
    -U

echo "✅ API key stored securely in macOS Keychain!"
echo ""
echo "📝 Next steps:"
echo "1. The API key is now stored in Keychain"
echo "2. Update your shell profile to export it:"
echo ""
echo "   Add this to ~/.zshrc (or ~/.bash_profile):"
echo "   export MERAKI_API_KEY=\$(security find-generic-password -a 'meraki-mcp' -s 'MERAKI_API_KEY' -w 2>/dev/null)"
echo ""
echo "3. Or manually set it for this session:"
echo "   export MERAKI_API_KEY=\$(security find-generic-password -a 'meraki-mcp' -s 'MERAKI_API_KEY' -w)"
echo ""
echo "4. Restart Cursor to load the MCP server with the secure API key"

