#!/usr/bin/env python3
"""
Categorize code issues from code-v13.md into:
1. Comment-only fixes (safe to fix immediately)
2. Minor UI/shared code fixes (safe to fix immediately)
3. Global changes affecting all UIs (needs review - add to code-global-v13.doc)
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

        # Find individual issues
        issue_blocks = re.findall(
            r'####\s*([^\n]+)\n\n\*\*Description:\*\*\s*([^\n]+)\n\n\*\*Affected files:\*\*\s*\n((?:- `[^`]+`\n)+)\n\*\*Details:\*\*\n(.*?)(?=\n---|\Z)',
            severity_content,
            re.DOTALL
        )

        for issue_type, description, files_raw, details in issue_blocks:
            files = re.findall(r'- `([^`]+)`', files_raw)

            issues.append({
                'severity': current_severity,
                'type': issue_type.strip(),
                'description': description.strip(),
                'files': files,
                'details': details.strip()
            })

    return issues


def categorize_issue(issue: Dict) -> str:
    """Categorize an issue as 'comment', 'safe', or 'global'."""

    files = issue['files']
    description = issue['description'].lower()
    details = issue['details'].lower()

    # Global files that affect all UIs - these need review
    global_files = [
        'src/interpreter.py',
        'src/runtime.py',
        'src/interactive.py',
        'src/immediate_executor.py',
        'src/parser.py',
        'src/lexer.py',
        'src/evaluator.py',
        'src/ast_nodes.py',
    ]

    # Check if any file is a global file
    for f in files:
        if any(f.endswith(gf) or gf in f for gf in global_files):
            # But if it's ONLY a comment fix, it's safe
            if 'comment' in description and 'code' not in description:
                if 'validation' not in details and 'implement' not in details:
                    return 'comment'
            return 'global'

    # Documentation files
    if all(f.startswith('docs/') for f in files):
        return 'safe'  # Documentation fixes are safe

    # Comment-only fixes
    if 'code_vs_comment' in issue['type'].lower():
        # Check if it's truly just a comment fix
        if 'validation' in details or 'missing' in details or 'bug' in details:
            # This reveals a code issue
            return 'global' if any(f.startswith('src/') and not f.startswith('src/ui/') for f in files) else 'safe'
        return 'comment'

    # UI-specific files
    ui_files = [f for f in files if 'src/ui/' in f or 'src/filesystem/' in f or 'src/file_io.py' in f]
    if ui_files:
        # Check if the issue is safe
        if 'security' in description or 'validation' in description:
            return 'global'  # Security issues need review
        return 'safe'

    # Default to global if unsure
    return 'global'


def main():
    input_file = Path('docs/history/code-v13.md')

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = parse_issues(content)

    # Categorize
    comment_issues = []
    safe_issues = []
    global_issues = []

    for issue in issues:
        category = categorize_issue(issue)
        if category == 'comment':
            comment_issues.append(issue)
        elif category == 'safe':
            safe_issues.append(issue)
        else:
            global_issues.append(issue)

    print(f"Total issues: {len(issues)}")
    print(f"Comment-only fixes: {len(comment_issues)}")
    print(f"Safe UI/shared fixes: {len(safe_issues)}")
    print(f"Global changes (need review): {len(global_issues)}")
    print()

    # Show categorization
    print("=== COMMENT-ONLY FIXES ===")
    for issue in comment_issues[:10]:
        print(f"- [{issue['severity']}] {issue['description'][:80]}...")
        print(f"  Files: {', '.join(issue['files'])}")
    if len(comment_issues) > 10:
        print(f"  ... and {len(comment_issues) - 10} more")
    print()

    print("=== SAFE UI/SHARED FIXES ===")
    for issue in safe_issues[:10]:
        print(f"- [{issue['severity']}] {issue['description'][:80]}...")
        print(f"  Files: {', '.join(issue['files'])}")
    if len(safe_issues) > 10:
        print(f"  ... and {len(safe_issues) - 10} more")
    print()

    print("=== GLOBAL CHANGES (NEED REVIEW) ===")
    for issue in global_issues[:10]:
        print(f"- [{issue['severity']}] {issue['description'][:80]}...")
        print(f"  Files: {', '.join(issue['files'])}")
    if len(global_issues) > 10:
        print(f"  ... and {len(global_issues) - 10} more")

    # Save categorized lists
    with open('docs/history/code-v13-categorized.txt', 'w', encoding='utf-8') as f:
        f.write("=== COMMENT-ONLY FIXES ===\n\n")
        for issue in comment_issues:
            f.write(f"[{issue['severity']}] {issue['description']}\n")
            f.write(f"Files: {', '.join(issue['files'])}\n\n")

        f.write("\n=== SAFE UI/SHARED FIXES ===\n\n")
        for issue in safe_issues:
            f.write(f"[{issue['severity']}] {issue['description']}\n")
            f.write(f"Files: {', '.join(issue['files'])}\n\n")

        f.write("\n=== GLOBAL CHANGES (NEED REVIEW) ===\n\n")
        for issue in global_issues:
            f.write(f"[{issue['severity']}] {issue['description']}\n")
            f.write(f"Files: {', '.join(issue['files'])}\n\n")

    print(f"\nSaved to docs/history/code-v13-categorized.txt")


if __name__ == '__main__':
    main()
