#!/usr/bin/env python3
"""
Query and filter parsed inconsistencies.

Usage examples:
  # Show all high severity issues
  python3 utils/query_inconsistencies.py --severity high

  # Show issues for a specific file
  python3 utils/query_inconsistencies.py --file src/interpreter.py

  # Show issues of a specific type
  python3 utils/query_inconsistencies.py --type code_vs_comment

  # Show issues matching a search term
  python3 utils/query_inconsistencies.py --search "GOTO"

  # Combine filters
  python3 utils/query_inconsistencies.py --severity high --file src/interpreter.py

  # Export to a new JSON file
  python3 utils/query_inconsistencies.py --severity high --output high_priority.json
"""

import json
import argparse
from pathlib import Path


def load_issues(file_path):
    """Load parsed inconsistencies JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def filter_issues(data, severity=None, file_filter=None, type_filter=None, search=None):
    """Filter issues based on criteria."""
    filtered = []

    severities = [severity] if severity else ['high', 'medium', 'low']

    for sev in severities:
        for issue in data['issues_by_severity'][sev]:
            # Apply filters
            if file_filter:
                if not any(file_filter in f for f in issue['affected_files']):
                    continue

            if type_filter:
                if type_filter.lower() not in issue['type'].lower():
                    continue

            if search:
                search_lower = search.lower()
                if not (search_lower in issue['description'].lower() or
                        search_lower in issue['details'].lower() or
                        search_lower in issue['type'].lower()):
                    continue

            filtered.append(issue)

    return filtered


def print_issue(issue, index=None, show_details=False):
    """Pretty print an issue."""
    if index is not None:
        print(f"\n{'=' * 80}")
        print(f"Issue #{index}")
        print('=' * 80)

    print(f"Severity: {issue['severity'].upper()}")
    print(f"Type: {issue['type']}")
    print(f"Description: {issue['description']}")
    print(f"Affected files:")
    for f in issue['affected_files']:
        print(f"  - {f}")

    if show_details:
        print(f"\nDetails:")
        print(issue['details'])


def main():
    parser = argparse.ArgumentParser(
        description='Query and filter parsed inconsistencies',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--file', '-f',
        help='Filter by file path (partial match)'
    )
    parser.add_argument(
        '--severity', '-s',
        choices=['high', 'medium', 'low'],
        help='Filter by severity'
    )
    parser.add_argument(
        '--type', '-t',
        help='Filter by issue type (partial match)'
    )
    parser.add_argument(
        '--search', '-q',
        help='Search in description, details, and type'
    )
    parser.add_argument(
        '--details', '-d',
        action='store_true',
        help='Show full details for each issue'
    )
    parser.add_argument(
        '--output', '-o',
        help='Save filtered results to JSON file'
    )
    parser.add_argument(
        '--count', '-c',
        action='store_true',
        help='Only show count, not full list'
    )
    parser.add_argument(
        '--input', '-i',
        default='docs/dev/parsed_inconsistencies.json',
        help='Input JSON file (default: docs/dev/parsed_inconsistencies.json)'
    )

    args = parser.parse_args()

    # Load data
    data = load_issues(args.input)

    # Filter
    filtered = filter_issues(
        data,
        severity=args.severity,
        file_filter=args.file,
        type_filter=args.type,
        search=args.search
    )

    # Output
    if args.count:
        print(f"Found {len(filtered)} issues")
        return

    print(f"\nFound {len(filtered)} matching issues\n")

    if args.output:
        # Save to file
        output_data = {
            'metadata': data['metadata'].copy(),
            'metadata_note': 'Filtered results',
            'filters': {
                'severity': args.severity,
                'file': args.file,
                'type': args.type,
                'search': args.search
            },
            'issues': filtered
        }
        output_data['metadata']['total_issues'] = len(filtered)

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {args.output}")
    else:
        # Print to console
        for i, issue in enumerate(filtered, 1):
            print_issue(issue, index=i, show_details=args.details)


if __name__ == '__main__':
    main()
