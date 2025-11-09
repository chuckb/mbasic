#!/usr/bin/env python3
"""
Bulk-import all issues from v14 (or v15) into the ignore file.

Use this if you reviewed a previous report and decided all issues were OK.
"""

import json
from pathlib import Path
from filter_existing_report import parse_markdown_report
from datetime import datetime
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 bulk_ignore_from_v14.py <v14|v15>")
        print("\nThis will mark ALL issues from the specified report as ignored.")
        return 1

    version = sys.argv[1]

    if version == 'v14':
        report_path = Path('../../docs/history/docs_inconsistencies_report-v14.md')
    elif version == 'v15':
        report_path = Path('../../docs/history/docs_inconsistencies_report-v15.md')
    else:
        print(f"Error: Unknown version '{version}'. Use 'v14' or 'v15'")
        return 1

    if not report_path.exists():
        print(f"Error: {report_path} not found")
        return 1

    # Load existing ignore file if it exists
    ignore_path = Path('.consistency_ignore.json')
    if ignore_path.exists():
        with open(ignore_path) as f:
            ignore_data = json.load(f)
        print(f"Loaded existing ignore file with {len(ignore_data.get('ignored_issues', {}))} issues")
    else:
        ignore_data = {
            '_comment': f'Bulk-imported from {version} review',
            'ignored_issues': {}
        }

    # Parse the report
    print(f"\nParsing {report_path.name}...")
    preamble, issues = parse_markdown_report(report_path)
    print(f"Found {len(issues)} issues in {version}")

    # Add all to ignore file
    added = 0
    already_ignored = 0

    for issue in issues:
        hash_val = issue['hash']
        if hash_val in ignore_data['ignored_issues']:
            already_ignored += 1
        else:
            ignore_data['ignored_issues'][hash_val] = {
                'description': issue['description'],
                'files': issue['files'],
                'details': issue.get('details', ''),
                'type': issue.get('type', ''),
                'reason': f'Bulk-imported from {version} (all reviewed as OK)',
                'reviewed_by': 'bulk_import',
                'reviewed_date': datetime.now().strftime('%Y-%m-%d')
            }
            added += 1

    # Save
    with open(ignore_path, 'w') as f:
        json.dump(ignore_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Bulk import complete!")
    print(f"  Added: {added} issues")
    print(f"  Already ignored: {already_ignored} issues")
    print(f"  Total in ignore file: {len(ignore_data['ignored_issues'])} issues")
    print(f"\nNow when you run check_docs_consistency3.py or filter v16:")
    print(f"  It will automatically filter these {len(ignore_data['ignored_issues'])} issues")
    print(f"  Only showing new issues that appeared after {version}")

    return 0

if __name__ == '__main__':
    exit(main())
