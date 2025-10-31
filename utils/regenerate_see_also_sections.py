#!/usr/bin/env python3
"""
Regenerate "See Also" sections in help documentation based on metadata.

This script:
1. Reads all function and statement markdown files
2. Extracts metadata (category, related)
3. Auto-generates "See Also" sections based on category groupings
4. Removes "not yet documented" placeholders
5. Updates all files with consistent, correct cross-references
"""

import re
from pathlib import Path
from typing import Dict, List, Set
import frontmatter

def parse_doc_file(filepath: Path) -> Dict:
    """Parse a markdown file and extract metadata."""
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    return {
        'path': filepath,
        'filename': filepath.stem,
        'category': post.metadata.get('category', 'NEEDS_CATEGORIZATION'),
        'title': post.metadata.get('title', filepath.stem.upper()),
        'type': post.metadata.get('type', 'unknown'),
        'related': post.metadata.get('related', []),
        'description': post.metadata.get('description', ''),
        'content': post.content
    }

def build_category_index(docs: List[Dict]) -> Dict[str, List[Dict]]:
    """Build an index of documents by category."""
    index = {}
    for doc in docs:
        category = doc['category']
        if category not in index:
            index[category] = []
        index[category].append(doc)
    return index

def generate_see_also_section(doc: Dict, category_index: Dict[str, List[Dict]]) -> str:
    """Generate a See Also section for a document."""
    related_docs = []

    # Get all docs in same category (excluding self)
    category = doc['category']
    if category in category_index:
        for other in category_index[category]:
            if other['filename'] != doc['filename']:
                related_docs.append(other)

    # Add explicitly related docs from metadata
    for related_name in doc['related']:
        # Find the doc by filename
        for other in all_docs:
            if other['filename'].lower() == related_name.lower():
                if other not in related_docs:
                    related_docs.append(other)

    if not related_docs:
        return ""

    # Sort by title
    related_docs.sort(key=lambda d: d['title'])

    # Generate markdown
    lines = ["## See Also\n"]
    for other in related_docs:
        # Determine link path (relative)
        if other['type'] == doc['type']:
            # Same type (both functions or both statements)
            link = f"{other['filename']}.md"
        else:
            # Different type - need to go up and into other directory
            if doc['type'] == 'function':
                link = f"../statements/{other['filename']}.md"
            else:
                link = f"../functions/{other['filename']}.md"

        desc = other['description'] if other['description'] else other['title']
        lines.append(f"- [{other['title']}]({link}) - {desc}\n")

    return "".join(lines)

def remove_old_see_also(content: str) -> str:
    """Remove existing See Also section from content."""
    # Match from ## See Also to end of file or next ## section
    pattern = r'## See Also\n.*?(?=\n##|\Z)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    # Remove trailing whitespace
    content = content.rstrip() + '\n'
    return content

def update_doc_file(doc: Dict, new_see_also: str):
    """Update a document file with new See Also section."""
    # Read file with frontmatter
    with open(doc['path'], 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    # Remove old See Also section
    content = remove_old_see_also(post.content)

    # Add new See Also section at end if we have one
    if new_see_also:
        content = content.rstrip() + '\n\n' + new_see_also

    # Write back
    with open(doc['path'], 'w', encoding='utf-8') as f:
        f.write('---\n')
        # Write frontmatter
        for key, value in post.metadata.items():
            if isinstance(value, list):
                f.write(f'{key}: {value}\n')
            elif isinstance(value, str) and ('\n' in value or ':' in value):
                f.write(f'{key}: "{value}"\n')
            else:
                f.write(f'{key}: {value}\n')
        f.write('---\n\n')
        f.write(content)

if __name__ == '__main__':
    # Find all function and statement docs
    help_root = Path('docs/help/common/language')

    functions_dir = help_root / 'functions'
    statements_dir = help_root / 'statements'

    all_docs = []

    # Parse all functions
    if functions_dir.exists():
        for filepath in functions_dir.glob('*.md'):
            if filepath.name != 'index.md':
                all_docs.append(parse_doc_file(filepath))

    # Parse all statements
    if statements_dir.exists():
        for filepath in statements_dir.glob('*.md'):
            if filepath.name != 'index.md':
                all_docs.append(parse_doc_file(filepath))

    print(f"Found {len(all_docs)} documentation files")

    # Build category index
    category_index = build_category_index(all_docs)

    print(f"Categories: {', '.join(sorted(category_index.keys()))}")

    # Generate and update See Also sections
    updated_count = 0
    removed_placeholders = 0

    for doc in all_docs:
        old_content = doc['content']

        # Check if has "not yet documented"
        if 'not yet documented' in old_content:
            removed_placeholders += 1

        # Generate new See Also section
        new_see_also = generate_see_also_section(doc, category_index)

        # Update file
        update_doc_file(doc, new_see_also)
        updated_count += 1

        if updated_count % 10 == 0:
            print(f"  Updated {updated_count} files...")

    print(f"\n✓ Updated {updated_count} files")
    print(f"✓ Removed {removed_placeholders} 'not yet documented' placeholders")
    print(f"\nAll 'See Also' sections have been regenerated based on categories!")
