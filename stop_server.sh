#!/bin/bash
# Helper script to gracefully stop the MCP server

echo "Looking for running MCP server processes..."

# Find Python processes running server.py
PIDS=$(pgrep -f "python.*server.py")

if [ -z "$PIDS" ]; then
    echo "No MCP server processes found."
    exit 0
fi

echo "Found server process(es): $PIDS"

for PID in $PIDS; do
    echo "Sending SIGINT to PID $PID..."
    kill -INT $PID
done

echo "Waiting for graceful shutdown..."
sleep 2

# Check if any are still running
REMAINING=$(pgrep -f "python.*server.py")

if [ -z "$REMAINING" ]; then
    echo "✅ All server processes stopped gracefully"
else
    echo "⚠️  Some processes still running: $REMAINING"
    echo "Use 'kill -9 $REMAINING' to force stop if needed"
fi
