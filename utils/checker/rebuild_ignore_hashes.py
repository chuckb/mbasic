#!/usr/bin/env python3
"""
Rebuild the ignore file with correct hashes.

The original ignore file has manually-created random hashes.
This script recomputes hashes based on description+files.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

# Import the stable hash computation
try:
    from compute_stable_hash import compute_stable_hash
except ImportError:
    print("Error: compute_stable_hash module not found")
    print("Make sure compute_stable_hash.py is in the same directory")
    import sys
    sys.exit(1)


def compute_issue_hash(description: str, files: list, details: str = "", issue_type: str = "") -> str:
    """Compute a stable hash for an issue.

    Uses stable data (files + details + type) instead of variable description text.
    """
    return compute_stable_hash(files, details, issue_type)

def main():
    ignore_file = Path(__file__).parent / '.consistency_ignore.json'
    backup_file = Path(__file__).parent / '.consistency_ignore.json.backup'

    if not ignore_file.exists():
        print(f"Error: {ignore_file} not found")
        return 1

    # Load the existing file
    with open(ignore_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    old_issues = data.get('ignored_issues', {})
    print(f"Loaded {len(old_issues)} issues with old hashes")

    # Backup the original
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Backed up to {backup_file.name}")

    # Rebuild with correct hashes
    new_issues = {}
    mismatches = 0

    for old_hash, info in old_issues.items():
        description = info.get('description', '')
        files = info.get('files', [])
        details = info.get('details', '')
        issue_type = info.get('type', '')

        if not files:
            print(f"Warning: Skipping entry with missing files: {old_hash}")
            continue

        # Compute the correct hash using stable hash
        new_hash = compute_issue_hash(description, files, details, issue_type)

        if new_hash != old_hash:
            mismatches += 1
            if mismatches <= 5:  # Show first 5 examples
                print(f"\nHash mismatch:")
                print(f"  Old: {old_hash}")
                print(f"  New: {new_hash}")
                print(f"  Desc: {description[:60]}...")
                print(f"  Details: {details[:60] if details else '(none)'}...")

        new_issues[new_hash] = info

    print(f"\nTotal hash mismatches: {mismatches}/{len(old_issues)}")
    print(f"Rebuilt {len(new_issues)} issues with correct hashes")

    # Save the new file
    new_data = {
        "_comment": f"Issues marked as reviewed/ignored. Hashes rebuilt on {datetime.now().strftime('%Y-%m-%d')}.",
        "ignored_issues": new_issues
    }

    with open(ignore_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved rebuilt ignore file to {ignore_file.name}")
    print(f"✓ Original backed up to {backup_file.name}")

    return 0

if __name__ == '__main__':
    exit(main())
