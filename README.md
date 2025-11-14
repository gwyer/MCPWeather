# MCP Weather Notes Server

[![GitHub](https://img.shields.io/github/license/gwyer/MCPWeather)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A minimal Model Context Protocol (MCP) server in Python that exposes three tools:

## Available Tools

1. **get_weather(city)** – Returns current weather using Open-Meteo API
   - Input: city name (string)
   - Output: temperature, wind speed, weather code, etc.

2. **save_note(text)** – Saves a note to local JSON file
   - Input: note text (string)
   - Output: saved note with ID and timestamp

3. **get_notes()** – Retrieves all saved notes from local storage
   - Input: none
   - Output: array of all notes with IDs, text, and timestamps

## Setup

See [SETUP_CLAUDE.md](SETUP_CLAUDE.md) for instructions on connecting to Claude Desktop.

## Testing

Run the test suite without an MCP client:
```bash
source .venv/bin/activate
python test_tools.py
```

## Running the Server

Start the server directly (for testing):
```bash
source .venv/bin/activate
python server.py
```

Stop the server gracefully with **Ctrl+C** (only one press needed).

For more details on stopping the server, see [STOPPING_SERVER.md](STOPPING_SERVER.md).

## Features

- ✅ Real-time weather data from Open-Meteo API
- ✅ Local JSON-based note storage
- ✅ Retrieve all saved notes
- ✅ Graceful shutdown handling
- ✅ Comprehensive error handling
- ✅ Full test suite included
- ✅ Works with Claude Desktop and Claude Code

## Requirements

- Python 3.11+
- Virtual environment (included)
- MCP-compatible client (Claude Desktop or Claude Code)

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with the [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic.