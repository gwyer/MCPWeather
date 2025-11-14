#!/usr/bin/env python3
# server.py
import asyncio
import json
import signal
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl
import mcp.server.stdio

from weather import get_weather_for_city
from notes_store import add_note, get_notes

# Create server instance
app = Server("weather-notes-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city using Open-Meteo API",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="save_note",
            description="Save a note to local JSON file",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The note text to save"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="get_notes",
            description="Retrieve all saved notes from local JSON file",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_weather":
        city = arguments.get("city")
        if not city:
            return [TextContent(type="text", text="Error: city parameter is required")]

        result = get_weather_for_city(city)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "save_note":
        text = arguments.get("text")
        if not text:
            return [TextContent(type="text", text="Error: text parameter is required")]

        result = add_note(text)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_notes":
        result = get_notes()
        if not result:
            return [TextContent(type="text", text="No notes found.")]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    else:
        return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]

async def main():
    """Run the MCP server using stdio transport with graceful shutdown."""
    # Setup for graceful shutdown
    shutdown_event = asyncio.Event()

    def signal_handler(sig, frame):
        """Handle shutdown signals gracefully."""
        print("\n[Server] Received shutdown signal, cleaning up...", file=sys.stderr)
        shutdown_event.set()

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print("[Server] MCP Weather Notes Server started", file=sys.stderr)
            print("[Server] Press Ctrl+C to stop", file=sys.stderr)

            # Create server task
            server_task = asyncio.create_task(
                app.run(
                    read_stream,
                    write_stream,
                    app.create_initialization_options()
                )
            )

            # Create shutdown monitor task
            shutdown_task = asyncio.create_task(shutdown_event.wait())

            # Wait for either server to finish or shutdown signal
            done, pending = await asyncio.wait(
                [server_task, shutdown_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            print("[Server] Shutdown complete", file=sys.stderr)

    except KeyboardInterrupt:
        print("\n[Server] Keyboard interrupt received, shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"[Server] Error: {e}", file=sys.stderr)
        raise
    finally:
        print("[Server] Server stopped", file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Server] Exiting...", file=sys.stderr)
        sys.exit(0)
