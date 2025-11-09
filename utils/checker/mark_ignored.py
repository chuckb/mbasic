#!/usr/bin/env python3
"""
Mark issues as ignored in consistency reports.

Usage:
    # Interactively mark issues from code-v14.md
    python3 utils/checker/mark_ignored.py docs/history/code-v14.md

    # Mark a specific issue by hash
    python3 utils/checker/mark_ignored.py --hash abc123 --reason "Platform limitation"

    # List all ignored issues
    python3 utils/checker/mark_ignored.py --list
"""

import json
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime


def compute_issue_hash(description: str, files: list) -> str:
    """Compute a stable hash for an issue based on description and files."""
    # Normalize the description and files for consistent hashing
    normalized = description.lower().strip() + "||" + "||".join(sorted(files))
    return hashlib.md5(normalized.encode()).hexdigest()[:12]


def load_ignore_file(ignore_path: Path) -> dict:
    """Load the ignore file."""
    if ignore_path.exists():
        with open(ignore_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {"_comment": "Issues marked as reviewed/ignored.", "ignored_issues": {}}


def save_ignore_file(ignore_path: Path, data: dict):
    """Save the ignore file."""
    with open(ignore_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_markdown_report(report_path: Path) -> list:
    """Parse a markdown report and extract issues."""
    issues = []
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by markdown headers (#### or ###)
    sections = re.split(r'\n#{3,4}\s+', content)

    for section in sections[1:]:  # Skip the preamble
        lines = section.split('\n')
        if not lines:
            continue

        title = lines[0].strip()

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
                    file_path = line.strip('- `')
                    files.append(file_path)
                elif line.startswith('**'):
                    break

        # Extract details
        details = []
        in_details = False
        for line in lines:
            if line.startswith('**Details:**'):
                in_details = True
                continue
            if in_details:
                if line.startswith('---') or line.startswith('**'):
                    break
                details.append(line)

        if description and files:
            issue_hash = compute_issue_hash(description, files)
            issues.append({
                'hash': issue_hash,
                'title': title,
                'description': description,
                'files': files,
                'details': '\n'.join(details).strip()
            })

    return issues


def interactive_mark_ignored(report_path: Path, ignore_path: Path):
    """Interactively mark issues as ignored."""
    issues = parse_markdown_report(report_path)
    ignore_data = load_ignore_file(ignore_path)

    print(f"\nFound {len(issues)} issues in {report_path.name}")
    print("=" * 80)

    for i, issue in enumerate(issues, 1):
        print(f"\n[{i}/{len(issues)}] {issue['title']}")
        print(f"Description: {issue['description']}")
        print(f"Files: {', '.join(issue['files'])}")
        print(f"Hash: {issue['hash']}")

        # Check if already ignored
        if issue['hash'] in ignore_data['ignored_issues']:
            existing = ignore_data['ignored_issues'][issue['hash']]
            print(f"⚠️  Already ignored: {existing['reason']}")
            response = input("Update reason? [y/N/q]: ").strip().lower()
            if response == 'q':
                break
            if response != 'y':
                continue
        else:
            response = input("Mark as ignored? [y/N/q/d(etails)]: ").strip().lower()
            if response == 'q':
                break
            if response == 'd':
                print("\nDetails:")
                print(issue['details'])
                response = input("Mark as ignored? [y/N/q]: ").strip().lower()
            if response != 'y':
                continue

        reason = input("Reason: ").strip()
        if not reason:
            print("Skipped (no reason provided)")
            continue

        ignore_data['ignored_issues'][issue['hash']] = {
            'description': issue['description'],
            'reason': reason,
            'reviewed_by': 'human',
            'reviewed_date': datetime.now().strftime('%Y-%m-%d'),
            'files': issue['files']
        }

        save_ignore_file(ignore_path, ignore_data)
        print(f"✓ Marked as ignored")

    print(f"\n✓ Saved to {ignore_path}")


def list_ignored(ignore_path: Path):
    """List all ignored issues."""
    ignore_data = load_ignore_file(ignore_path)
    ignored = ignore_data.get('ignored_issues', {})

    if not ignored:
        print("No ignored issues")
        return

    print(f"\n{len(ignored)} ignored issues:")
    print("=" * 80)

    for issue_hash, info in ignored.items():
        print(f"\nHash: {issue_hash}")
        print(f"Description: {info['description']}")
        print(f"Reason: {info['reason']}")
        if 'reviewed_date' in info and 'reviewed_by' in info:
            print(f"Reviewed: {info['reviewed_date']} by {info['reviewed_by']}")
        print(f"Files: {', '.join(info.get('files', []))}")


def main():
    parser = argparse.ArgumentParser(
        description='Mark consistency issues as ignored',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'report',
        nargs='?',
        help='Path to markdown report file to process'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all ignored issues'
    )
    parser.add_argument(
        '--hash',
        help='Hash of issue to mark as ignored'
    )
    parser.add_argument(
        '--reason',
        help='Reason for ignoring (used with --hash)'
    )

    args = parser.parse_args()

    # Find ignore file
    script_dir = Path(__file__).parent
    ignore_path = script_dir / '.consistency_ignore.json'

    if args.list:
        list_ignored(ignore_path)
    elif args.hash:
        if not args.reason:
            print("Error: --reason required when using --hash")
            return 1

        ignore_data = load_ignore_file(ignore_path)
        ignore_data['ignored_issues'][args.hash] = {
            'description': f'Manual entry ({args.hash})',
            'reason': args.reason,
            'reviewed_by': 'human',
            'reviewed_date': datetime.now().strftime('%Y-%m-%d'),
            'files': []
        }
        save_ignore_file(ignore_path, ignore_data)
        print(f"✓ Marked {args.hash} as ignored")
    elif args.report:
        report_path = Path(args.report)
        if not report_path.exists():
            print(f"Error: {report_path} not found")
            return 1
        interactive_mark_ignored(report_path, ignore_path)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
