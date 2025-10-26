#!/usr/bin/env python3
"""
Enhance front matter metadata by replacing placeholders with content-based descriptions.

This script reads markdown files, extracts useful information from the content,
and generates appropriate descriptions and keywords.
"""

from pathlib import Path
import frontmatter
import re
from typing import Dict, List, Set

def extract_purpose(content: str) -> str:
    """Extract purpose/description from ## Purpose or ## Description section."""
    # Look for Purpose section
    purpose_match = re.search(r'##\s+Purpose\s*\n+(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if purpose_match:
        purpose = purpose_match.group(1).strip()
        # Take first sentence or paragraph
        first_sentence = re.split(r'[.\n]', purpose)[0].strip()
        return first_sentence

    # Look for Description section
    desc_match = re.search(r'##\s+Description\s*\n+(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if desc_match:
        desc = desc_match.group(1).strip()
        first_sentence = re.split(r'[.\n]', desc)[0].strip()
        return first_sentence

    return None

def extract_syntax(content: str) -> str:
    """Extract syntax from code block in Syntax section."""
    syntax_match = re.search(r'##\s+Syntax\s*\n+```(?:basic)?\s*\n(.*?)\n```', content, re.DOTALL | re.IGNORECASE)
    if syntax_match:
        syntax = syntax_match.group(1).strip()
        # Take first line if multi-line
        first_line = syntax.split('\n')[0].strip()
        # Remove BASIC-style comments and version notes
        first_line = re.sub(r'Versions?:.*', '', first_line).strip()
        return first_line
    return None

def extract_keywords_from_content(content: str, title: str) -> Set[str]:
    """Extract potential keywords from content."""
    keywords = set()

    # Add title words
    title_words = re.findall(r'\w+', title.lower())
    keywords.update([w for w in title_words if len(w) > 2 and w not in ['the', 'and', 'for']])

    # Look for common BASIC terms
    basic_terms = [
        'print', 'input', 'read', 'data', 'goto', 'gosub', 'return',
        'for', 'next', 'if', 'then', 'else', 'while', 'wend',
        'dim', 'array', 'string', 'number', 'variable',
        'file', 'open', 'close', 'field', 'get', 'put',
        'function', 'statement', 'operator', 'command',
        'loop', 'condition', 'branch', 'subroutine',
        'error', 'line', 'program', 'execute'
    ]

    content_lower = content.lower()
    for term in basic_terms:
        if term in content_lower:
            keywords.add(term)

    # Extract from Remarks/Purpose sections
    remarks_match = re.search(r'##\s+(?:Remarks|Purpose|Description)\s*\n+(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if remarks_match:
        remarks = remarks_match.group(1).lower()
        # Extract important words (capitalized or in quotes)
        important = re.findall(r'\b[A-Z][A-Z]+\b|\b(?:the |a |an )?(\w+) (?:statement|function|command|operator)\b', remarks)
        keywords.update([w.lower() for w in important if isinstance(w, str) and len(w) > 2])

    return keywords

def enhance_file(file_path: Path, dry_run: bool = True) -> bool:
    """Enhance metadata for a single file."""
    try:
        with open(file_path, 'r') as f:
            post = frontmatter.load(f)

        # Check if enhancement needed
        needs_desc = post.get('description') == 'NEEDS_DESCRIPTION'
        needs_keywords = post.get('keywords') == ['NEEDS_KEYWORDS']

        if not (needs_desc or needs_keywords):
            return False

        changed = False
        content = post.content
        title = post.get('title', file_path.stem)

        # Extract description if needed
        if needs_desc:
            purpose = extract_purpose(content)
            if purpose:
                post['description'] = purpose
                changed = True
                print(f"  Description: {purpose[:60]}...")

        # Extract keywords if needed
        if needs_keywords:
            keywords = extract_keywords_from_content(content, title)
            if keywords:
                post['keywords'] = sorted(list(keywords))[:10]  # Top 10
                changed = True
                print(f"  Keywords: {', '.join(sorted(list(keywords))[:5])}...")

        # Add syntax if available and not present
        if not post.get('syntax'):
            syntax = extract_syntax(content)
            if syntax:
                post['syntax'] = syntax
                changed = True
                print(f"  Syntax: {syntax[:60]}...")

        if changed and not dry_run:
            with open(file_path, 'w') as f:
                f.write(frontmatter.dumps(post))

        return changed

    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    """Process all help files with placeholder metadata."""
    import argparse

    parser = argparse.ArgumentParser(description='Enhance help file metadata')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--path', default='docs/help', help='Help directory path')
    args = parser.parse_args()

    help_root = Path(args.path)

    # Find all files with placeholders
    files_to_enhance = []

    for md_file in help_root.rglob('*.md'):
        if md_file.name in ['index.md', 'search_index.json']:
            continue

        try:
            with open(md_file, 'r') as f:
                post = frontmatter.load(f)

            if (post.get('description') == 'NEEDS_DESCRIPTION' or
                post.get('keywords') == ['NEEDS_KEYWORDS']):
                files_to_enhance.append(md_file)
        except:
            pass

    print(f"Found {len(files_to_enhance)} files needing enhancement")
    print()

    if args.dry_run:
        print("DRY RUN - no files will be modified")
        print()

    enhanced_count = 0
    for file_path in files_to_enhance:
        rel_path = file_path.relative_to(help_root)
        print(f"Processing: {rel_path}")

        if enhance_file(file_path, dry_run=args.dry_run):
            enhanced_count += 1
        else:
            print("  (no changes)")
        print()

    print(f"\nEnhanced {enhanced_count} of {len(files_to_enhance)} files")

    if args.dry_run:
        print("\nRun without --dry-run to apply changes")

if __name__ == '__main__':
    main()
