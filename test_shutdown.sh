#!/bin/bash
# Test script to verify graceful shutdown of MCP server

echo "Testing MCP Server Graceful Shutdown"
echo "======================================"
echo ""
echo "Starting server in background..."

source .venv/bin/activate

# Start server in background and capture PID
python server.py &
SERVER_PID=$!

echo "Server started with PID: $SERVER_PID"
echo "Waiting 2 seconds..."
sleep 2

echo ""
echo "Sending SIGINT (Ctrl+C equivalent)..."
kill -INT $SERVER_PID

echo "Waiting for graceful shutdown (max 3 seconds)..."
TIMEOUT=3
COUNTER=0

while kill -0 $SERVER_PID 2>/dev/null && [ $COUNTER -lt $TIMEOUT ]; do
    sleep 0.5
    COUNTER=$((COUNTER + 1))
done

if kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ FAILED: Server did not shut down gracefully within ${TIMEOUT} seconds"
    echo "Forcing shutdown with SIGKILL..."
    kill -9 $SERVER_PID
    exit 1
else
    echo "✅ SUCCESS: Server shut down gracefully!"
    exit 0
fi
