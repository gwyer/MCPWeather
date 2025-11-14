# How to Stop the MCP Server

The MCP server now includes graceful shutdown handling to ensure clean exits.

## Method 1: Using Ctrl+C (Recommended)

When running the server directly (not through Claude Desktop):

```bash
python server.py
```

To stop it:
1. Press **Ctrl+C** once
2. Wait 1-2 seconds for graceful shutdown
3. You should see: `[Server] Shutdown complete`

The server will now shut down cleanly on the first Ctrl+C without hanging.

## Method 2: Using the Helper Script

If you have orphaned server processes:

```bash
./stop_server.sh
```

This script will:
- Find all running MCP server processes
- Send graceful shutdown signals
- Report if any processes failed to stop

## Method 3: Manual Process Management

### Find the server process:
```bash
ps aux | grep "python.*server.py"
```

### Send graceful shutdown signal:
```bash
kill -INT <PID>
```

### If that doesn't work, force kill:
```bash
kill -9 <PID>
```

## When Running via Claude Desktop

When the MCP server is running through Claude Desktop:
- The server lifecycle is managed by Claude Desktop
- Closing Claude Desktop will automatically stop the server
- No manual intervention needed

## Improvements Made

The updated `server.py` now includes:

1. **Signal Handlers**
   - Catches SIGINT (Ctrl+C) and SIGTERM signals
   - Triggers graceful shutdown instead of abrupt exit

2. **Task Cancellation**
   - Properly cancels async tasks
   - Cleans up resources before exit

3. **Status Messages**
   - Shows startup confirmation
   - Reports shutdown progress
   - Logs errors to stderr

## Troubleshooting

### Server won't stop with Ctrl+C

Try these steps:
1. Press Ctrl+C and wait 3 seconds
2. If still running, use `./stop_server.sh`
3. As a last resort, use `kill -9 <PID>`

### Finding stuck processes

```bash
# List all Python server processes
pgrep -fl "python.*server.py"

# Kill all at once (use with caution)
pkill -INT -f "python.*server.py"
```

### Server logs showing errors during shutdown

This is normal behavior. The MCP protocol may log connection errors when the stdio streams are closed during shutdown. These can be safely ignored.

## Testing Shutdown Behavior

Run the automated test:
```bash
./test_shutdown.sh
```

This will:
- Start the server in background
- Wait 2 seconds
- Send shutdown signal
- Verify graceful exit
- Report success/failure
