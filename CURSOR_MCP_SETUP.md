# 🔐 Secure Cursor MCP Configuration Guide

This guide shows you how to securely configure the Meraki MCP server in Cursor without hardcoding your API key.

## Security Best Practices

✅ **DO:**
- Store API keys in environment variables
- Use macOS Keychain for secure storage
- Keep API keys out of version control
- Use separate keys for different environments

❌ **DON'T:**
- Hardcode API keys in configuration files
- Commit API keys to git
- Share API keys in plain text
- Use the same key across multiple projects

## Setup Options

### Option 1: macOS Keychain (Recommended) 🔒

This is the most secure option for macOS users.

#### Step 1: Store API Key in Keychain

Run the setup script:

```bash
chmod +x setup_meraki_api_key.sh
./setup_meraki_api_key.sh
```

Or manually store it:

```bash
security add-generic-password \
    -a "meraki-mcp" \
    -s "MERAKI_API_KEY" \
    -w "your_actual_api_key_here" \
    -U
```

#### Step 2: Export from Keychain in Shell Profile

Add this to your `~/.zshrc` (or `~/.bash_profile`):

```bash
# Load Meraki API Key from Keychain
export MERAKI_API_KEY=$(security find-generic-password -a 'meraki-mcp' -s 'MERAKI_API_KEY' -w 2>/dev/null)
```

Then reload your shell:

```bash
source ~/.zshrc
```

#### Step 3: Update Cursor MCP Config

The MCP configuration file at:
```
~/Library/Application Support/Cursor/User/globalStorage/mcp.json
```

Should reference the environment variable. Cursor will automatically pick up environment variables from your shell when it launches.

**Note:** If Cursor doesn't pick up the environment variable automatically, you may need to:
1. Set it in Cursor's launch environment, or
2. Use Option 2 below with a wrapper script

### Option 2: Environment Variable in Shell Profile

#### Step 1: Add to Shell Profile

Add to `~/.zshrc` (or `~/.bash_profile`):

```bash
export MERAKI_API_KEY="your_actual_api_key_here"
```

#### Step 2: Reload Shell

```bash
source ~/.zshrc
```

#### Step 3: Verify

```bash
echo $MERAKI_API_KEY
```

**⚠️ Security Note:** This stores the key in plain text in your shell profile. Use Option 1 (Keychain) for better security.

### Option 3: .env File (For Local Development)

#### Step 1: Create .env File

Create a `.env` file in the project root:

```bash
echo "MERAKI_API_KEY=your_actual_api_key_here" > .env
```

**Note:** `.env` is already in `.gitignore`, so it won't be committed.

#### Step 2: Use with Docker Compose

If using `docker-compose`, it will automatically load `.env`:

```bash
docker-compose up -d
```

#### Step 3: For Cursor MCP

Cursor MCP config can't directly read `.env` files, so you'll need to export it:

```bash
export $(cat .env | xargs)
```

Then restart Cursor.

### Option 4: Direct Environment Variable in Cursor Config (Less Secure)

If the above options don't work, you can set it directly in the MCP config, but this is less secure:

```json
{
  "mcpServers": {
    "Meraki MCP": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--pull=always",
        "meraki-mcp:latest"
      ],
      "env": {
        "MERAKI_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

**⚠️ Warning:** This stores the key in plain text. Only use if other options don't work, and ensure the config file has proper permissions:

```bash
chmod 600 ~/Library/Application\ Support/Cursor/User/globalStorage/mcp.json
```

## Verifying Your Setup

1. **Check environment variable:**
   ```bash
   echo $MERAKI_API_KEY
   ```

2. **Test Docker container:**
   ```bash
   docker run --rm -e MERAKI_API_KEY=$MERAKI_API_KEY meraki-mcp:latest
   ```

3. **Restart Cursor** and test with a query like:
   - "What Meraki organizations do I have access to?"

## Troubleshooting

### Cursor doesn't see the environment variable

Cursor may not inherit environment variables from your shell. Try:

1. **Launch Cursor from terminal:**
   ```bash
   open -a Cursor
   ```

2. **Or use a wrapper script** that sets the environment before launching Docker.

### Keychain access issues

If you get keychain access errors:

```bash
# Check if the key exists
security find-generic-password -a "meraki-mcp" -s "MERAKI_API_KEY"

# Update access permissions
security set-generic-password-partition-list -a "meraki-mcp" -s "MERAKI_API_KEY" -T "/Applications/Cursor.app"
```

## Security Checklist

- [ ] API key is NOT in version control
- [ ] API key is NOT hardcoded in config files (or properly secured)
- [ ] Using Keychain or secure environment variable storage
- [ ] Config file has restricted permissions (600)
- [ ] Using separate API keys for dev/prod if applicable
- [ ] Regularly rotating API keys

## Additional Resources

- [Meraki Dashboard API Documentation](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API)
- [MCP Security Best Practices](https://modelcontextprotocol-security.io)
- [macOS Keychain Guide](https://support.apple.com/guide/keychain-access/)

