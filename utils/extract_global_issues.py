#!/usr/bin/env python3
"""
Extract global issues from code-v13.md that affect interpreter/runtime/interactive
and write them to code-global-v13.doc for review.
"""

import re
from pathlib import Path
from typing import List, Dict

def parse_issues(content: str) -> List[Dict]:
    """Parse issues from the markdown file."""
    issues = []

    # Split by severity sections
    severity_pattern = r'(### 🔴 High Severity|### 🟡 Medium Severity|### 🟢 Low Severity)'
    sections = re.split(severity_pattern, content)

    current_severity = None
    for i in range(1, len(sections), 2):
        if i + 1 >= len(sections):
            break

        severity_header = sections[i]
        severity_content = sections[i + 1]

        if '🔴' in severity_header:
            current_severity = 'High'
        elif '🟡' in severity_header:
            current_severity = 'Medium'
        elif '🟢' in severity_header:
            current_severity = 'Low'

        # Find individual issues - more flexible pattern
        issue_pattern = r'####\s*([^\n]+)\n+(.*?)(?=\n####|\n###|\Z)'
        issue_matches = re.findall(issue_pattern, severity_content, re.DOTALL)

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
                'severity': current_severity,
                'type': issue_type.strip(),
                'description': description.strip(),
                'files': files,
                'details': details,
                'full_text': f'#### {issue_type}\n\n{issue_body}\n---'
            })

    return issues


def is_global_issue(issue: Dict) -> bool:
    """Determine if an issue affects global code (interpreter/runtime/etc)."""

    files = issue['files']

    # Global files that affect all UIs
    global_files = [
        'src/interpreter.py',
        'src/runtime.py',
        'src/interactive.py',
        'src/immediate_executor.py',
        'src/parser.py',
        'src/lexer.py',
        'src/evaluator.py',
        'src/ast_nodes.py',
        'src/filesystem/sandboxed_fs.py',  # Security critical
        'src/settings.py',  # Settings affect all UIs
    ]

    # Check if any file is a global file
    for f in files:
        if any(gf in f for gf in global_files):
            return True

    # Also check for multi-file issues involving backend/base
    if any('base.py' in f or 'backend' in f for f in files):
        return True

    return False


def main():
    input_file = Path('docs/history/code-v13.md')
    output_file = Path('docs/history/code-global-v13.doc')

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = parse_issues(content)
    global_issues = [issue for issue in issues if is_global_issue(issue)]

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Global Code Changes Requiring Review (v13)\n\n")
        f.write("Generated from code-v13.md\n")
        f.write("Contains: Changes to interpreter/runtime/interactive and other global code\n")
        f.write("These changes affect ALL UIs and require careful review before implementation\n\n")
        f.write(f"Total global issues: {len(global_issues)}\n\n")

        # Group by severity
        for severity in ['High', 'Medium', 'Low']:
            severity_issues = [i for i in global_issues if i['severity'] == severity]
            if not severity_issues:
                continue

            if severity == 'High':
                f.write("### 🔴 High Severity\n\n")
            elif severity == 'Medium':
                f.write("### 🟡 Medium Severity\n\n")
            else:
                f.write("### 🟢 Low Severity\n\n")

            for issue in severity_issues:
                f.write(f"{issue['full_text']}\n")

    print(f"Extracted {len(global_issues)} global issues to {output_file}")

    # Also print summary
    print("\n=== GLOBAL ISSUES SUMMARY ===")
    for issue in global_issues:
        print(f"[{issue['severity']}] {issue['description'][:80]}...")
        print(f"  Files: {', '.join(issue['files'][:3])}")
        if len(issue['files']) > 3:
            print(f"        ... and {len(issue['files']) - 3} more")


if __name__ == '__main__':
    main()
