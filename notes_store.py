# notes_store.py
import json, os, time
from pathlib import Path

# Use absolute path to ensure notes.json is always in the same location
SCRIPT_DIR = Path(__file__).parent.resolve()
FILE = SCRIPT_DIR / "notes.json"

def add_note(text: str):
    """Add a note to the notes.json file with proper error handling."""
    notes = []

    # Read existing notes if file exists
    if FILE.exists():
        try:
            with open(FILE, "r") as f:
                notes = json.load(f)
        except json.JSONDecodeError:
            # If file is corrupted, start fresh
            notes = []
        except PermissionError as e:
            raise PermissionError(f"Cannot read {FILE}: {e}")

    # Create new note entry
    entry = {"id": len(notes)+1, "text": text, "ts": time.time()}
    notes.append(entry)

    # Write notes back to file
    try:
        with open(FILE, "w") as f:
            json.dump(notes, f, indent=2)
    except PermissionError as e:
        raise PermissionError(f"Cannot write to {FILE}: {e}")

    return entry

def get_notes():
    """Retrieve all notes from the notes.json file."""
    # Return empty list if file doesn't exist
    if not FILE.exists():
        return []

    # Read and return all notes
    try:
        with open(FILE, "r") as f:
            notes = json.load(f)
        return notes
    except json.JSONDecodeError:
        # If file is corrupted, return empty list
        return []
    except PermissionError as e:
        raise PermissionError(f"Cannot read {FILE}: {e}")
