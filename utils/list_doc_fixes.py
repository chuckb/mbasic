#!/usr/bin/env python3
"""
Extract actionable documentation fixes from code-v13.md.
Groups them by file for efficient batch processing.
"""

import re
from pathlib import Path
from collections import defaultdict

def parse_issues(content: str):
    """Parse issues from code-v13.md."""
    issues = []

    # Find individual issues
    issue_pattern = r'####\s*([^\n]+)\n+(.*?)(?=\n####|\n###|\Z)'
    issue_matches = re.findall(issue_pattern, content, re.DOTALL)

    for issue_type, issue_body in issue_matches:
        # Extract description
        desc_match = re.search(r'\*\*Description:\*\*\s*([^\n]+)', issue_body)
        if not desc_match:
            continue
        description = desc_match.group(1).strip()

        # Extract files
        files_match = re.search(r'\*\*Affected files:\*\*\s*\n((?:- `[^`]+`\n)+)', issue_body)
        if not files_match:
            continue
        files = re.findall(r'- `([^`]+)`', files_match.group(1))

        # Extract details
        details_match = re.search(r'\*\*Details:\*\*\s*\n(.*?)(?=\n---|\Z)', issue_body, re.DOTALL)
        details = details_match.group(1).strip() if details_match else ''

        issues.append({
            'type': issue_type.strip(),
            'description': description,
            'files': files,
            'details': details
        })

    return issues


def main():
    input_file = Path('docs/history/code-v13.md')

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = parse_issues(content)

    # Filter documentation issues only
    doc_issues = [i for i in issues if all(f.startswith('docs/') for f in i['files'])]

    print(f"Total documentation issues: {len(doc_issues)}\n")

    # Group by file
    by_file = defaultdict(list)
    for issue in doc_issues:
        for file in issue['files']:
            by_file[file].append(issue)

    # Print by file
    print("=== DOCUMENTATION ISSUES BY FILE ===\n")
    for file in sorted(by_file.keys()):
        print(f"\n{file} ({len(by_file[file])} issues)")
        print("-" * 80)
        for issue in by_file[file]:
            print(f"  • {issue['description'][:100]}...")
            if len(issue['details']) < 200:
                print(f"    Details: {issue['details'][:150]}")

    # Save detailed report
    with open('docs/history/code-v13-doc-fixes.txt', 'w', encoding='utf-8') as f:
        f.write(f"Documentation Fixes from code-v13.md\n")
        f.write(f"Total issues: {len(doc_issues)}\n")
        f.write("=" * 80 + "\n\n")

        for file in sorted(by_file.keys()):
            f.write(f"\n{'='*80}\n")
            f.write(f"FILE: {file}\n")
            f.write(f"{'='*80}\n\n")

            for i, issue in enumerate(by_file[file], 1):
                f.write(f"{i}. {issue['description']}\n")
                f.write(f"   Type: {issue['type']}\n\n")
                f.write(f"   {issue['details']}\n")
                f.write(f"\n{'-'*80}\n\n")

    print(f"\n\nDetailed report saved to docs/history/code-v13-doc-fixes.txt")


if __name__ == '__main__':
    main()
