#!/usr/bin/env python3
"""
Check all markdown links in help documentation for broken references.

This script validates that all relative links in .md files point to existing files.
Run this before committing documentation changes to catch broken links.

Usage:
    python3 utils/check_help_links.py
"""

import re
from pathlib import Path
import sys


def find_markdown_links(content: str) -> list:
    """Extract all markdown links from content.

    Returns list of tuples: (link_text, link_target)
    """
    # Match [text](target) format
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, content)


def resolve_link(source_file: Path, link_target: str, help_root: Path) -> Path:
    """Resolve a link target to an absolute path.

    Args:
        source_file: The markdown file containing the link
        link_target: The link target from markdown (e.g., "foo.md" or "../bar.md")
        help_root: The root help directory

    Returns:
        Resolved absolute path
    """
    # Skip external links (http://, https://, mailto:)
    if link_target.startswith(('http://', 'https://', 'mailto:', '#')):
        return None

    # Remove anchor fragments (#section)
    if '#' in link_target:
        link_target = link_target.split('#')[0]
        if not link_target:  # Just an anchor, no file
            return None

    # Absolute paths (relative to help root)
    if link_target.startswith('/'):
        return help_root / link_target.lstrip('/')

    # Relative paths - resolve from source file's directory
    return (source_file.parent / link_target).resolve()


def check_file_links(md_file: Path, help_root: Path) -> list:
    """Check all links in a markdown file.

    Returns list of broken links as tuples: (link_text, link_target, resolved_path)
    """
    broken_links = []

    try:
        content = md_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not read {md_file}: {e}")
        return []

    links = find_markdown_links(content)

    for link_text, link_target in links:
        resolved = resolve_link(md_file, link_target, help_root)

        # Skip external links
        if resolved is None:
            continue

        # Check if target exists
        if not resolved.exists():
            broken_links.append((link_text, link_target, resolved))

    return broken_links


def main():
    """Check all help documentation for broken links."""
    # Find project root (parent of utils/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    help_root = project_root / 'docs' / 'help'

    if not help_root.exists():
        print(f"Error: Help directory not found at {help_root}")
        return 1

    print(f"Checking links in {help_root}")
    print("-" * 80)

    # Find all markdown files
    md_files = list(help_root.rglob('*.md'))
    print(f"Found {len(md_files)} markdown files")
    print()

    total_links = 0
    total_broken = 0
    files_with_broken = []

    for md_file in sorted(md_files):
        broken = check_file_links(md_file, help_root)

        if broken:
            rel_path = md_file.relative_to(help_root)
            files_with_broken.append((rel_path, broken))
            total_broken += len(broken)

    # Report results
    if files_with_broken:
        print(f"❌ Found {total_broken} broken link(s) in {len(files_with_broken)} file(s):")
        print()

        for rel_path, broken_links in files_with_broken:
            print(f"  {rel_path}:")
            for link_text, link_target, resolved in broken_links:
                print(f"    • [{link_text}]({link_target})")
                print(f"      → {resolved}")
                print(f"      (File does not exist)")
            print()

        return 1
    else:
        print("✅ All links are valid!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
