#!/usr/bin/env python3
"""
Standalone test script to verify the MCP server tools work correctly
without needing to connect to an MCP client.
"""
import json
from weather import get_weather_for_city
from notes_store import add_note, get_notes

def test_weather():
    """Test the get_weather tool"""
    print("=" * 60)
    print("Testing get_weather tool")
    print("=" * 60)

    cities = ["London", "New York", "Tokyo", "Paris"]

    for city in cities:
        print(f"\nFetching weather for {city}...")
        try:
            result = get_weather_for_city(city)
            print(json.dumps(result, indent=2))

            if "error" not in result:
                print(f"✓ Successfully retrieved weather for {city}")
                print(f"  Temperature: {result.get('temperature', 'N/A')}°C")
                print(f"  Wind Speed: {result.get('windspeed', 'N/A')} km/h")
            else:
                print(f"✗ Error: {result['error']}")
        except Exception as e:
            print(f"✗ Exception occurred: {e}")

    print()

def test_notes():
    """Test the save_note tool"""
    print("=" * 60)
    print("Testing save_note tool")
    print("=" * 60)

    test_notes = [
        "Meeting scheduled for tomorrow at 10 AM",
        "Remember to buy groceries",
        "Project deadline: Friday",
        "Call dentist for appointment"
    ]

    for note_text in test_notes:
        print(f"\nSaving note: '{note_text}'")
        try:
            result = add_note(note_text)
            print(json.dumps(result, indent=2))
            print(f"✓ Note saved with ID: {result['id']}")
        except Exception as e:
            print(f"✗ Exception occurred: {e}")

    print()

def test_get_notes():
    """Test the get_notes tool"""
    print("=" * 60)
    print("Testing get_notes tool")
    print("=" * 60)

    print("\nRetrieving all saved notes...")
    try:
        notes = get_notes()
        print(f"✓ Successfully retrieved {len(notes)} notes")

        if notes:
            print("\nFirst 3 notes:")
            for note in notes[:3]:
                print(f"  - ID {note['id']}: {note['text'][:50]}...")
        else:
            print("  (No notes found)")

    except Exception as e:
        print(f"✗ Exception occurred: {e}")

    print()

def test_invalid_city():
    """Test error handling with invalid city"""
    print("=" * 60)
    print("Testing error handling")
    print("=" * 60)

    print("\nTrying to fetch weather for non-existent city...")
    result = get_weather_for_city("XYZ123InvalidCity")
    print(json.dumps(result, indent=2))

    if "error" in result:
        print("✓ Error handling works correctly")
    else:
        print("✗ Expected an error but got valid response")

    print()

if __name__ == "__main__":
    print("\n🧪 MCP Weather Notes Server - Standalone Test\n")

    # Run tests
    test_weather()
    test_notes()
    test_get_notes()
    test_invalid_city()

    print("=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\nTo view saved notes, check the 'notes.json' file")
    print("To run the MCP server: python server.py")
    print()
