#!/usr/bin/env python3
"""
Migrate old ignore file (with legacy hashes) to v16 with stable hashes.

This script:
1. Loads the old ignore file (21 issues with description-based hashes)
2. Parses v16 to find matching issues
3. Creates new ignore file with stable hashes
"""

import json
from pathlib import Path
from filter_existing_report import parse_markdown_report

def find_matching_issue(old_issue, v16_issues):
    """Find a matching issue in v16 based on files and description similarity."""
    old_files = set(old_issue.get('files', []))
    old_desc = old_issue.get('description', '').lower()

    # First try exact file match
    for issue in v16_issues:
        issue_files = set(issue.get('files', []))
        if old_files == issue_files:
            # Check if descriptions are similar
            issue_desc = issue.get('description', '').lower()
            # Match if first 30 chars are same
            if old_desc[:30] == issue_desc[:30]:
                return issue

    # Then try partial description match
    for issue in v16_issues:
        issue_desc = issue.get('description', '').lower()
        # Match if significant portion of description matches
        if len(old_desc) > 20 and old_desc[:20] in issue_desc:
            return issue

    return None

def main():
    # Load old ignore file
    old_ignore_path = Path('.consistency_ignore.json.old-legacy')
    if not old_ignore_path.exists():
        print(f"Error: {old_ignore_path} not found")
        return 1

    with open(old_ignore_path) as f:
        old_ignore = json.load(f)

    old_issues = old_ignore.get('ignored_issues', {})
    print(f"Loaded {len(old_issues)} issues from old ignore file")

    # Parse v16
    v16_path = Path('../../docs/history/docs_inconsistencies_report-v16.md')
    if not v16_path.exists():
        print(f"Error: {v16_path} not found")
        return 1

    print(f"\nParsing v16 report...")
    preamble, v16_issues = parse_markdown_report(v16_path)
    print(f"Found {len(v16_issues)} issues in v16")

    # Find matches
    new_ignore = {
        '_comment': 'Migrated from old ignore file to stable hashes for v16',
        'ignored_issues': {}
    }

    matched = 0
    not_found = 0

    print("\nMatching old issues to v16...")
    for old_hash, old_info in old_issues.items():
        print(f"\nOld: {old_info.get('description', '')[:60]}...")

        matching_issue = find_matching_issue(old_info, v16_issues)

        if matching_issue:
            # Use the new hash from v16
            new_hash = matching_issue['hash']
            new_ignore['ignored_issues'][new_hash] = {
                'description': matching_issue['description'],
                'files': matching_issue['files'],
                'details': matching_issue.get('details', ''),
                'type': matching_issue.get('type', ''),
                'reason': old_info.get('reason', 'Migrated from old ignore file'),
                'reviewed_by': old_info.get('reviewed_by', 'migration'),
                'reviewed_date': old_info.get('reviewed_date', '2025-11-09'),
                'migrated_from_hash': old_hash
            }
            matched += 1
            print(f"  ✓ Matched in v16 (new hash: {new_hash})")
        else:
            not_found += 1
            print(f"  ✗ Not found in v16 (issue may have been fixed)")

    # Save new ignore file
    output_path = Path('.consistency_ignore.json')
    with open(output_path, 'w') as f:
        json.dump(new_ignore, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Migration complete!")
    print(f"  Matched: {matched}/{len(old_issues)} issues")
    print(f"  Not in v16: {not_found}/{len(old_issues)} issues")
    print(f"  Saved to: {output_path}")
    print(f"\nNow run:")
    print(f"  python3 filter_existing_report.py ../../docs/history/docs_inconsistencies_report-v16.md")
    print(f"  This should filter {matched} issues")

    return 0

if __name__ == '__main__':
    exit(main())
