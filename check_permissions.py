#!/usr/bin/env python3
"""
Diagnostic script to check file permissions for the MCP server
"""
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
NOTES_FILE = SCRIPT_DIR / "notes.json"

def check_permissions():
    """Check read/write permissions for the notes file and directory"""

    print("=" * 60)
    print("MCP Server Permission Diagnostic")
    print("=" * 60)

    # Check directory
    print(f"\n📁 Directory: {SCRIPT_DIR}")
    print(f"   Exists: {SCRIPT_DIR.exists()}")
    print(f"   Readable: {os.access(SCRIPT_DIR, os.R_OK)}")
    print(f"   Writable: {os.access(SCRIPT_DIR, os.W_OK)}")
    print(f"   Executable: {os.access(SCRIPT_DIR, os.X_OK)}")

    # Check notes.json file
    print(f"\n📄 Notes file: {NOTES_FILE}")
    print(f"   Exists: {NOTES_FILE.exists()}")

    if NOTES_FILE.exists():
        print(f"   Readable: {os.access(NOTES_FILE, os.R_OK)}")
        print(f"   Writable: {os.access(NOTES_FILE, os.W_OK)}")

        # Get file stats
        stat_info = NOTES_FILE.stat()
        print(f"   Permissions: {oct(stat_info.st_mode)[-3:]}")
        print(f"   Owner UID: {stat_info.st_uid}")
        print(f"   Owner GID: {stat_info.st_gid}")
    else:
        print(f"   Can create: {os.access(SCRIPT_DIR, os.W_OK)}")

    # Check current process
    print(f"\n🔧 Current Process:")
    print(f"   User ID: {os.getuid()}")
    print(f"   Group ID: {os.getgid()}")
    print(f"   Effective User ID: {os.geteuid()}")
    print(f"   Effective Group ID: {os.getegid()}")

    # Test write operation
    print(f"\n✍️  Write Test:")
    try:
        from notes_store import add_note
        result = add_note("Permission check test note")
        print(f"   ✓ Successfully wrote test note (ID: {result['id']})")
        return 0
    except PermissionError as e:
        print(f"   ✗ Permission Error: {e}")
        return 1
    except Exception as e:
        print(f"   ✗ Unexpected Error: {e}")
        return 1
    finally:
        print()

if __name__ == "__main__":
    sys.exit(check_permissions())
