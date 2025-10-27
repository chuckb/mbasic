#!/usr/bin/env python3
"""
Clean PDF extraction artifacts from help documentation.

Removes page headers like:
- BASIC-80 COMMANDS AND STATEMENTS Page X-Y
- BASIC-SO COMMANDS AND STATEMENTS Page X-Y
- Any variations of these patterns
"""

import re
from pathlib import Path
from typing import List, Tuple


def clean_page_headers(content: str) -> Tuple[str, int]:
    """
    Remove page header artifacts from markdown content.

    Returns:
        (cleaned_content, num_removals)
    """
    lines = content.split('\n')
    cleaned_lines = []
    removals = 0

    # Patterns to remove
    patterns = [
        r'BASIC-\d+\s+COMMANDS\s+AND\s+STATEMENTS\s+Page\s+\d+-\d+',
        r'BASIC-[A-Z]+\s+COMMANDS\s+AND\s+STATEMENTS\s+Page\s+\d+-\d+',
        r'COMMANDS\s+AND\s+STATEMENTS\s+Page\s+\d+-\d+',
        r'Page\s+\d+-\d+\s+BASIC-\d+\s+COMMANDS',
        r'Page\s+\d+-\d+\s+BASIC-[A-Z]+\s+COMMANDS',
    ]

    for line in lines:
        # Check if line matches any removal pattern
        should_remove = False
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                should_remove = True
                removals += 1
                break

        if not should_remove:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines), removals


def clean_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Clean a single markdown file.

    Returns:
        (was_modified, num_removals)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        cleaned_content, removals = clean_page_headers(original_content)

        if removals > 0:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
            return True, removals

        return False, 0

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Clean PDF extraction artifacts from help documentation'
    )
    parser.add_argument(
        'path',
        type=Path,
        nargs='?',
        default=Path('docs/help'),
        help='Path to help directory (default: docs/help)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without modifying files'
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path not found: {args.path}")
        return 1

    print("=" * 70)
    print("Cleaning PDF Artifacts from Help Documentation")
    print("=" * 70)

    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be modified\n")

    # Find all markdown files
    md_files = list(args.path.rglob('*.md'))
    print(f"\nScanning {len(md_files)} markdown files...")

    modified_files = []
    total_removals = 0

    for md_file in md_files:
        was_modified, removals = clean_file(md_file, dry_run=args.dry_run)

        if was_modified:
            rel_path = md_file.relative_to(args.path)
            modified_files.append((rel_path, removals))
            total_removals += removals

            status = "Would clean" if args.dry_run else "Cleaned"
            print(f"  {status}: {rel_path} ({removals} artifacts removed)")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if modified_files:
        print(f"\n{'Would modify' if args.dry_run else 'Modified'}: {len(modified_files)} files")
        print(f"Total artifacts removed: {total_removals}")

        if not args.dry_run:
            print("\n✅ Cleanup complete!")
            print("\nNext steps:")
            print("  1. Review changes: git diff docs/help")
            print("  2. Rebuild help indexes: python3 utils/build_docs.py")
            print("  3. Commit changes: git add docs/help && git commit")
    else:
        print("\n✅ No artifacts found - documentation is clean!")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
