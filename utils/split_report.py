#!/usr/bin/env python3
"""
Split docs_inconsistencies_report-v13.md into:
- docs-v13.md: Documentation/comment changes only (no code behavior changes)
- code-v13.md: Code behavior changes (actual functionality fixes)
"""

import re
from pathlib import Path

def categorize_issue(issue_text: str, issue_type: str, description: str) -> str:
    """
    Determine if an issue is documentation-only or requires code changes.

    Returns: 'docs' or 'code'
    """

    # Convert to lowercase for matching
    desc_lower = description.lower()
    issue_lower = issue_text.lower()

    # Strong indicators this is CODE behavior change needed
    code_indicators = [
        'security warning about user_id validation is in docstring but not enforced in code',
        'missing validation',
        'not enforced',
        'security-critical',
        'validation checks that don\'t match',
        'logic error',
        'logic seems backwards',
        'resetting to halted would lose',
        'missing implementation',
        'stub but',
        'missing error handling',
        'incorrect implementation',
        'does not validate',
        'no validation',
        'bug',
        'broken',
        'fails',
        'error in code',
        'code error',
        'implementation gap',
        'missing check',
        'missing feature',
        'not implemented',
        'incorrect behavior',
        'wrong behavior',
        'should raise',
        'should return',
        'should validate',
        'security issue',
        'vulnerability',
    ]

    # Check if this is a code behavior issue
    for indicator in code_indicators:
        if indicator in desc_lower or indicator in issue_lower:
            return 'code'

    # Strong indicators this is DOCS-only change
    docs_indicators = [
        'comment',
        'docstring',
        'documentation',
        'docs',
        'terminology',
        'naming',
        'description',
        'explanation',
        'unclear comment',
        'misleading comment',
        'outdated comment',
        'incorrect comment',
        'comment claims',
        'comment says',
        'comment states',
        'comment describes',
        'docstring claims',
        'docstring says',
        'docstring states',
    ]

    # If issue type is explicitly about comments/docs
    if 'code_vs_comment' in issue_type.lower():
        # But check if it's revealing a code bug
        if any(indicator in desc_lower for indicator in code_indicators):
            return 'code'
        return 'docs'

    if 'documentation inconsistency' in issue_type.lower():
        # Check if documentation is wrong but code is right
        if 'code is correct' in issue_lower or 'implementation is correct' in issue_lower:
            return 'docs'
        # Check if this reveals a code bug
        if any(indicator in desc_lower for indicator in code_indicators):
            return 'code'
        # Default to docs for pure documentation issues
        return 'docs'

    # Default: if mostly about comments/docs, it's docs
    docs_count = sum(1 for indicator in docs_indicators if indicator in desc_lower)
    code_count = sum(1 for indicator in code_indicators if indicator in desc_lower)

    if docs_count > code_count:
        return 'docs'

    # When in doubt, it's probably a code issue
    return 'code'


def split_report(input_file: Path, docs_file: Path, code_file: Path):
    """Split the report into documentation and code changes."""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into individual issues
    # Issues are separated by "---" and have a structure like:
    # #### {type}
    # **Description:** {description}
    # ... details ...
    # ---

    # First, split into header and issues sections
    lines = content.split('\n')

    # Find where issues start (after "### 🔴 High Severity")
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('### 🔴 High Severity'):
            header_end = i
            break

    header = '\n'.join(lines[:header_end])
    issues_content = '\n'.join(lines[header_end:])

    # Split issues by severity level
    severity_pattern = r'(### 🔴 High Severity|### 🟡 Medium Severity|### 🟢 Low Severity)'
    severity_sections = re.split(severity_pattern, issues_content)

    # Reconstruct with proper grouping
    docs_issues = []
    code_issues = []

    for i in range(1, len(severity_sections), 2):
        if i + 1 >= len(severity_sections):
            break

        severity_header = severity_sections[i]
        severity_content = severity_sections[i + 1]

        # Split this severity section into individual issues
        # Issues start with #### and end with ---
        issue_pattern = r'(####[^\n]+\n(?:.*?\n)*?---)'
        issues = re.findall(issue_pattern, severity_content, re.MULTILINE)

        docs_severity_issues = []
        code_severity_issues = []

        for issue in issues:
            # Extract issue type and description
            type_match = re.search(r'####\s*(.+)', issue)
            desc_match = re.search(r'\*\*Description:\*\*\s*(.+)', issue)

            if not type_match or not desc_match:
                continue

            issue_type = type_match.group(1).strip()
            description = desc_match.group(1).strip()

            # Categorize
            category = categorize_issue(issue, issue_type, description)

            if category == 'docs':
                docs_severity_issues.append(issue)
            else:
                code_severity_issues.append(issue)

        # Add to respective lists with severity headers if we have issues
        if docs_severity_issues:
            if not docs_issues or docs_issues[-1] != severity_header:
                docs_issues.append(severity_header + '\n')
            docs_issues.extend(docs_severity_issues)

        if code_severity_issues:
            if not code_issues or code_issues[-1] != severity_header:
                code_issues.append(severity_header + '\n')
            code_issues.extend(code_severity_issues)

    # Create output files
    docs_header = """# Documentation Changes (v13)

Generated by splitting docs_inconsistencies_report-v13.md
Contains: Documentation and comment fixes (no code behavior changes)

## 📋 Documentation Inconsistencies

"""

    code_header = """# Code Behavior Changes (v13)

Generated by splitting docs_inconsistencies_report-v13.md
Contains: Code changes that affect behavior, validation, security, or implementation

## 🔧 Code Issues Requiring Fixes

"""

    with open(docs_file, 'w', encoding='utf-8') as f:
        f.write(docs_header)
        f.write('\n'.join(docs_issues))

    with open(code_file, 'w', encoding='utf-8') as f:
        f.write(code_header)
        f.write('\n'.join(code_issues))

    # Count issues
    docs_count = len([i for i in docs_issues if i.strip().startswith('####')])
    code_count = len([i for i in code_issues if i.strip().startswith('####')])

    print(f"Split complete:")
    print(f"  Documentation issues: {docs_count}")
    print(f"  Code behavior issues: {code_count}")
    print(f"  Total: {docs_count + code_count}")


if __name__ == '__main__':
    input_file = Path('docs/history/docs_inconsistencies_report-v13.md')
    docs_file = Path('docs/history/docs-v13.md')
    code_file = Path('docs/history/code-v13.md')

    split_report(input_file, docs_file, code_file)
