#!/usr/bin/env python3
"""
Filter an existing consistency report using the ignore file.

Usage:
    python3 filter_existing_report.py docs/history/docs_inconsistencies_report-v16.md
"""

import sys
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime

# Import the stable hash computation
try:
    from compute_stable_hash import compute_stable_hash
except ImportError:
    print("Error: compute_stable_hash module not found")
    print("Make sure compute_stable_hash.py is in the same directory")
    sys.exit(1)


def compute_issue_hash(description: str, files: list, details: str = "", issue_type: str = "") -> str:
    """Compute a stable hash for an issue.

    Uses stable data (files + details + type) instead of variable description text.
    """
    return compute_stable_hash(files, details, issue_type)


def load_ignore_file(ignore_path: Path) -> dict:
    """Load the ignore file."""
    if ignore_path.exists():
        with open(ignore_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('ignored_issues', {})
    return {}


def parse_markdown_report(report_path: Path) -> tuple:
    """Parse a markdown report and extract issues.

    Returns: (preamble, issues_list)
    """
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where the actual issues start (after the header)
    # Look for the first ### or #### header
    match = re.search(r'\n(#{2,4}\s+)', content)
    if match:
        preamble_end = match.start()
        preamble = content[:preamble_end]
        issues_section = content[preamble_end:]
    else:
        # No sections found, treat everything as preamble
        return content, []

    # Split by section headers
    # Match ### or #### but not ## (which is top-level like "## Summary")
    sections = re.split(r'\n(#{3,4}\s+.+)', issues_section)

    issues = []
    current_section_header = None

    for i, section in enumerate(sections):
        # Check if this is a header
        if re.match(r'^#{3,4}\s+', section):
            current_section_header = section
            continue

        # Skip empty sections
        if not section.strip():
            continue

        # This is content under a header
        if current_section_header is None:
            continue

        # Extract title from section header (the #### line)
        # current_section_header is like "#### code_vs_comment"
        title = current_section_header.replace('#', '').strip() if current_section_header else ""

        # Parse the content
        lines = section.split('\n')

        # Extract description
        description = None
        for line in lines:
            if line.startswith('**Description:**'):
                description = line.replace('**Description:**', '').strip()
                break

        # Extract affected files
        files = []
        in_files_section = False
        for line in lines:
            if line.startswith('**Affected files:**'):
                in_files_section = True
                continue
            if in_files_section:
                if line.startswith('- `') and line.endswith('`'):
                    file_path = line.strip('- `').strip('`')
                    files.append(file_path)
                elif line.startswith('**') or line.startswith('---'):
                    break

        # Extract details text (same as in mark_ignored.py)
        details_lines = []
        in_details = False
        for line in lines:
            if line.startswith('**Details:**'):
                in_details = True
                continue
            if in_details:
                if line.startswith('---') or line.startswith('**'):
                    break
                details_lines.append(line)

        details_text = '\n'.join(details_lines).strip()

        # If we have files, compute hash
        if files:
            issue_hash = compute_issue_hash(description, files, details_text, title)

            # Store the full section (header + content)
            full_section = current_section_header + '\n' + section

            issues.append({
                'hash': issue_hash,
                'description': description,
                'files': files,
                'details': details_text,
                'type': title,
                'section_header': current_section_header,
                'section_content': section,
                'full_text': full_section
            })

    return preamble, issues


def filter_and_save_report(report_path: Path, ignore_file: Path, output_path: Path = None):
    """Filter a report and save the filtered version."""

    # Load ignore file
    ignored_issues = load_ignore_file(ignore_file)
    print(f"Loaded {len(ignored_issues)} ignored issues")

    # Parse the report
    print(f"\nParsing {report_path.name}...")
    preamble, issues = parse_markdown_report(report_path)
    print(f"Found {len(issues)} issues in report")

    # Filter issues
    kept_issues = []
    filtered_issues = []

    for issue in issues:
        if issue['hash'] in ignored_issues:
            filtered_issues.append(issue)
            print(f"  ✓ Filtering: {issue['description'][:60]}... (hash: {issue['hash']})")
        else:
            kept_issues.append(issue)

    print(f"\n📊 Results:")
    print(f"  Total issues: {len(issues)}")
    print(f"  Kept: {len(kept_issues)}")
    print(f"  Filtered: {len(filtered_issues)}")

    # Determine output path
    if output_path is None:
        # Create output filename based on input
        # v16.md -> v16-filtered.md
        stem = report_path.stem  # e.g., "docs_inconsistencies_report-v16"
        if stem.endswith('-filtered'):
            output_path = report_path  # Overwrite
        else:
            output_path = report_path.parent / f"{stem}-filtered.md"

    # Write filtered report
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write preamble with note about filtering
        f.write(preamble)
        f.write(f"\n**Note:** This report has been filtered to remove {len(filtered_issues)} ")
        f.write(f"previously reviewed/ignored issues. Original report had {len(issues)} total issues.\n")

        # Write kept issues
        if kept_issues:
            # Group by severity if possible
            # Look for severity markers in section headers
            high = [i for i in kept_issues if '🔴' in i['section_header'] or 'High' in i['section_header']]
            medium = [i for i in kept_issues if '🟡' in i['section_header'] or 'Medium' in i['section_header']]
            low = [i for i in kept_issues if '🟢' in i['section_header'] or 'Low' in i['section_header']]
            other = [i for i in kept_issues if i not in high and i not in medium and i not in low]

            if high:
                f.write("\n### 🔴 High Severity\n\n")
                for issue in high:
                    f.write(issue['section_content'])
                    f.write("\n")

            if medium:
                f.write("\n### 🟡 Medium Severity\n\n")
                for issue in medium:
                    f.write(issue['section_content'])
                    f.write("\n")

            if low:
                f.write("\n### 🟢 Low Severity\n\n")
                for issue in low:
                    f.write(issue['section_content'])
                    f.write("\n")

            if other:
                f.write("\n### Other Issues\n\n")
                for issue in other:
                    f.write(issue['full_text'])
                    f.write("\n")
        else:
            f.write("\n✅ No new issues found! All issues have been reviewed.\n")

        # Update summary
        f.write(f"\n## Summary\n\n")
        f.write(f"- Total issues in filtered report: {len(kept_issues)}\n")
        f.write(f"- Issues filtered out (already reviewed): {len(filtered_issues)}\n")
        f.write(f"- Original total: {len(issues)}\n")
        f.write(f"\nFiltered on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"\n✅ Filtered report saved to: {output_path}")
    print(f"   Original: {len(issues)} issues")
    print(f"   Filtered: {len(kept_issues)} issues")
    print(f"   Removed: {len(filtered_issues)} issues")

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 filter_existing_report.py <report_path> [output_path]")
        print("\nExample:")
        print("  python3 filter_existing_report.py docs/history/docs_inconsistencies_report-v16.md")
        print("  python3 filter_existing_report.py ../../docs/history/docs_inconsistencies_report-v16.md")
        return 1

    report_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not report_path.exists():
        print(f"Error: {report_path} not found")
        return 1

    # Find ignore file
    ignore_file = Path(__file__).parent / '.consistency_ignore.json'
    if not ignore_file.exists():
        print(f"Warning: {ignore_file} not found - no filtering will be done")
        return 1

    filter_and_save_report(report_path, ignore_file, output_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
