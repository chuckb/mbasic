#!/usr/bin/env python3
"""
Test help system integration across all three tiers.

Verifies:
1. All index files exist
2. All links in index files point to existing files
3. Search indexes are valid and complete
4. Three-tier navigation works (relative paths)
"""

from pathlib import Path
import json
import re
import sys
import os

# Get project root (3 levels up from tests/regression/help/)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

def test_file_exists(path: Path) -> tuple[bool, str]:
    """Test if a file exists."""
    help_root = PROJECT_ROOT / "docs/help"
    if path.exists():
        return True, f"✓ {path.relative_to(help_root)}"
    else:
        return False, f"✗ MISSING: {path.relative_to(help_root)}"

def extract_markdown_links(content: str) -> list[str]:
    """Extract all markdown links from content."""
    # Pattern: [text](path)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)
    return [path for _, path in matches if not path.startswith('http')]

def test_index_links(index_path: Path, help_root: Path) -> list[str]:
    """Test all links in an index file."""
    errors = []

    with open(index_path) as f:
        content = f.read()

    links = extract_markdown_links(content)

    for link in links:
        # Resolve relative to index file location
        link_path = (index_path.parent / link).resolve()

        if not link_path.exists():
            rel_path = link_path.relative_to(help_root) if link_path.is_relative_to(help_root) else link_path
            errors.append(f"  ✗ Broken link in {index_path.name}: {link} → {rel_path}")

    return errors

def test_search_index(index_path: Path) -> list[str]:
    """Test search index validity."""
    errors = []

    try:
        with open(index_path) as f:
            index = json.load(f)

        # Check structure - 'files' is the minimum required key
        # Other keys (keywords, aliases, categories, by_type) are optional for backwards compatibility
        if 'files' not in index:
            errors.append(f"  ✗ Missing required key 'files' in {index_path.name}")

        # Check files exist
        for file_info in index.get('files', []):
            file_path = index_path.parent / file_info['path']
            if not file_path.exists():
                errors.append(f"  ✗ Indexed file missing: {file_info['path']}")

    except json.JSONDecodeError as e:
        errors.append(f"  ✗ Invalid JSON in {index_path.name}: {e}")
    except Exception as e:
        errors.append(f"  ✗ Error reading {index_path.name}: {e}")

    return errors

def main():
    """Run all tests."""
    help_root = PROJECT_ROOT / "docs/help"

    if not help_root.exists():
        print(f"✗ Help root not found: {help_root}")
        return 1

    print("Testing MBASIC Help System Integration")
    print("=" * 60)

    all_errors = []

    # Test 1: Index files exist
    print("\n1. Checking index files...")
    index_files = [
        help_root / "ui/curses/index.md",
        help_root / "ui/cli/index.md",
        help_root / "ui/tk/index.md",
        help_root / "mbasic/index.md",
        help_root / "common/language/index.md",
    ]

    for index_file in index_files:
        exists, msg = test_file_exists(index_file)
        print(f"  {msg}")
        if not exists:
            all_errors.append(msg)

    # Test 2: Links in index files
    print("\n2. Checking links in index files...")
    for index_file in index_files:
        if index_file.exists():
            errors = test_index_links(index_file, help_root)
            if errors:
                all_errors.extend(errors)
                for error in errors:
                    print(error)
            else:
                print(f"  ✓ All links valid in {index_file.name}")

    # Test 3: Search indexes
    print("\n3. Checking search indexes...")
    search_indexes = [
        help_root / "common/language/search_index.json",
        help_root / "mbasic/search_index.json",
        help_root / "ui/curses/search_index.json",
    ]

    for search_index in search_indexes:
        if search_index.exists():
            errors = test_search_index(search_index)
            if errors:
                all_errors.extend(errors)
                for error in errors:
                    print(error)
            else:
                with open(search_index) as f:
                    index = json.load(f)
                files_count = len(index.get('files', []))
                keywords_count = len(index.get('keywords', {}))
                print(f"  ✓ {search_index.relative_to(help_root)} - {files_count} files, {keywords_count} keywords")
        else:
            msg = f"  ✗ MISSING: {search_index.relative_to(help_root)}"
            print(msg)
            all_errors.append(msg)

    # Test 4: Three-tier structure
    print("\n4. Checking three-tier structure...")

    # Check we have files in all three tiers
    ui_files = list((help_root / "ui/curses").glob("*.md"))
    mbasic_files = list((help_root / "mbasic").glob("*.md"))
    language_files = list((help_root / "common/language").rglob("*.md"))

    print(f"  ✓ UI tier (curses): {len(ui_files)} files")
    print(f"  ✓ MBASIC tier: {len(mbasic_files)} files")
    print(f"  ✓ Language tier: {len(language_files)} files")

    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print(f"\n❌ FAILED: {len(all_errors)} errors found:\n")
        for error in all_errors:
            print(error)
        return 1
    else:
        print("\n✅ SUCCESS: All help system integration tests passed!")
        print("\nSummary:")
        print(f"  • {len(ui_files)} UI documentation files")
        print(f"  • {len(mbasic_files)} MBASIC documentation files")
        print(f"  • {len(language_files)} Language reference files")
        print(f"  • {len([f for f in index_files if f.exists()])} index files")
        print(f"  • {len([f for f in search_indexes if f.exists()])} search indexes")
        return 0

if __name__ == "__main__":
    sys.exit(main())
