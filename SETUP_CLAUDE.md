# Connecting MCP Weather Server to Claude

This guide shows you how to connect your MCP Weather Notes Server to Claude Desktop or Claude Code.

## Prerequisites

- Claude Desktop app installed, OR
- Claude Code CLI installed
- Python virtual environment set up (already done in this project)

## Configuration

### For Claude Desktop (macOS)

1. **Locate the Claude Desktop config file:**
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. **Edit the config file** and add your MCP server:

   ```json
   {
     "mcpServers": {
       "weather-notes": {
         "command": "python",
         "args": [
           "/Users/cg/PycharmProjects/MCPWeather/server.py"
         ],
         "env": {
           "VIRTUAL_ENV": "/Users/cg/PycharmProjects/MCPWeather/.venv"
         }
       }
     }
   }
   ```

   **Note:** If the file doesn't exist, create it with the above content. If it exists and has other servers, add the "weather-notes" entry to the existing "mcpServers" object.

3. **Restart Claude Desktop** for the changes to take effect.

4. **Verify the connection:**
   - Open Claude Desktop
   - Look for the MCP tools icon (usually a hammer/wrench icon)
   - You should see three tools available:
     - `get_weather` - Get current weather for a city
     - `save_note` - Save a note to local JSON file
     - `get_notes` - Retrieve all saved notes

### For Claude Code (CLI)

1. **Locate the Claude Code config file:**
   ```
   ~/.config/claude-code/mcp_settings.json
   ```

2. **Edit the config file** and add your MCP server:

   ```json
   {
     "mcpServers": {
       "weather-notes": {
         "command": "python",
         "args": [
           "/Users/cg/PycharmProjects/MCPWeather/server.py"
         ],
         "env": {
           "VIRTUAL_ENV": "/Users/cg/PycharmProjects/MCPWeather/.venv"
         }
       }
     }
   }
   ```

3. **Restart Claude Code** (if running).

## Quick Setup Script (macOS)

Run this command to automatically add the server to Claude Desktop:

```bash
mkdir -p ~/Library/Application\ Support/Claude
cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'
{
  "mcpServers": {
    "weather-notes": {
      "command": "python",
      "args": [
        "/Users/cg/PycharmProjects/MCPWeather/server.py"
      ],
      "env": {
        "VIRTUAL_ENV": "/Users/cg/PycharmProjects/MCPWeather/.venv"
      }
    }
  }
}
EOF
```

**⚠️ Warning:** This will overwrite your existing config. If you already have other MCP servers configured, manually edit the file instead.

## Testing the Connection

Once connected, try these prompts in Claude:

1. **Test weather tool:**
   ```
   What's the weather like in Tokyo?
   ```

2. **Test note-taking:**
   ```
   Save a note: "Remember to test the MCP server integration"
   ```

3. **Test retrieving notes:**
   ```
   Show me all my saved notes
   ```

4. **Combine all tools:**
   ```
   Check the weather in Paris, save a note about it, then show me all my notes.
   ```

## Troubleshooting

### Server not appearing in Claude

1. Check that the config file path is correct
2. Verify the Python path points to your virtual environment
3. Ensure the server.py path is absolute (not relative)
4. Restart Claude Desktop/Code completely

### Permission errors

Make sure server.py is executable:
```bash
chmod +x /Users/cg/PycharmProjects/MCPWeather/server.py
```

### Python import errors

Verify dependencies are installed in the virtual environment:
```bash
source /Users/cg/PycharmProjects/MCPWeather/.venv/bin/activate
pip list | grep mcp
```

### View MCP server logs

Check Claude's logs for MCP connection issues:
- **Claude Desktop:** `~/Library/Logs/Claude/`
- **Claude Code:** Check the console output

## Alternative: Using uv (Python Package Manager)

If you have `uv` installed, you can use this simpler config:

```json
{
  "mcpServers": {
    "weather-notes": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/cg/PycharmProjects/MCPWeather",
        "run",
        "server.py"
      ]
    }
  }
}
```

This automatically handles the virtual environment.

## Stopping the Server

When running the server directly (not via Claude Desktop):
- Press **Ctrl+C** once to stop gracefully
- The server now handles shutdown properly without hanging

For more details, see [STOPPING_SERVER.md](STOPPING_SERVER.md).

## Next Steps

- Check `notes.json` to see saved notes from Claude
- Extend the server with more tools (e.g., delete notes, search notes)
- Add more weather data (forecasts, multiple days, etc.)
