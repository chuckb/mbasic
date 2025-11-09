#!/usr/bin/env python3
"""Quick test to verify ignore system works correctly."""

import sys
import json
import hashlib
from pathlib import Path

# Import modules
sys.path.insert(0, str(Path(__file__).parent))
from mark_ignored import compute_issue_hash, load_ignore_file
from compute_stable_hash import compute_stable_hash

def test_hash_consistency():
    """Test that hash computation matches between both scripts."""
    print("Testing hash computation consistency...")

    test_cases = [
        {
            'description': 'SandboxedFileIO methods documented as STUB but list_files() is IMPLEMENTED',
            'files': ['src/file_io.py']
        },
        {
            'description': 'The auto_save.py module is fully implemented',
            'files': ['src/ui/auto_save.py']
        },
        {
            'description': 'Multiple files test',
            'files': ['src/file1.py', 'src/file2.py', 'src/file3.py']
        }
    ]

    # We can't initialize EnhancedConsistencyAnalyzer without API key
    # So we'll test the mark_ignored function directly and check ignore file
    ignore_file = Path(__file__).parent / '.consistency_ignore.json'
    ignore_data = load_ignore_file(ignore_file)

    print(f"\nLoaded {len(ignore_data.get('ignored_issues', {}))} ignored issues")

    for i, test in enumerate(test_cases, 1):
        hash1 = compute_issue_hash(test['description'], test['files'])
        print(f"\n{i}. Description: {test['description'][:60]}...")
        print(f"   Files: {test['files']}")
        print(f"   Hash: {hash1}")

        # Check if it's in the ignore file
        if hash1 in ignore_data.get('ignored_issues', {}):
            print(f"   ✓ Found in ignore file")
        else:
            print(f"   ✗ Not in ignore file")

    print("\n" + "="*60)
    print("Sample of first 5 hashes from ignore file:")
    for i, (hash_val, data) in enumerate(list(ignore_data.get('ignored_issues', {}).items())[:5], 1):
        print(f"\n{i}. Hash: {hash_val}")
        print(f"   Description: {data.get('description', '')[:60]}...")
        print(f"   Files: {data.get('files', [])}")

        # Recompute hash to verify
        recomputed = compute_issue_hash(data.get('description', ''), data.get('files', []))
        if recomputed == hash_val:
            print(f"   ✓ Hash matches")
        else:
            print(f"   ✗ Hash mismatch! Recomputed: {recomputed}")

if __name__ == '__main__':
    test_hash_consistency()
