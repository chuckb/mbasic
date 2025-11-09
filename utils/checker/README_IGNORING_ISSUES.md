# Ignoring/Suppressing Consistency Issues

The consistency checker now supports marking issues as "reviewed/ignored" so they don't appear in future scans.

## Quick Start

### Mark issues interactively from a report:
```bash
python3 utils/checker/mark_ignored.py docs/history/code-v14.md
```

This will walk through each issue and let you mark them as ignored with a reason.

### List all ignored issues:
```bash
python3 utils/checker/mark_ignored.py --list
```

### Mark a specific issue by hash:
```bash
python3 utils/checker/mark_ignored.py --hash abc123def --reason "Platform limitation"
```

## How It Works

1. **Issue Hashing**: Each issue is identified by a hash computed from its description and affected files
2. **Ignore File**: Ignored issues are stored in `utils/checker/.consistency_ignore.json`
3. **Filtering**: When generating a report, the checker automatically filters out ignored issues
4. **Reporting**: The report header shows how many issues were filtered

## Interactive Marking

When you run `mark_ignored.py` interactively, you'll see:

```
[1/23] Code vs Documentation inconsistency
Description: SandboxedFileIO methods documented as STUB but list_files() is IMPLEMENTED
Files: src/file_io.py
Hash: abc123def456

Mark as ignored? [y/N/q/d(etails)]:
```

Options:
- `y` - Mark as ignored (will prompt for reason)
- `N` - Skip this issue
- `q` - Quit interactive mode
- `d` - Show full details before deciding

## Example Reasons

Good reasons for ignoring issues:
- `"Already verified - documentation matches implementation"`
- `"Platform limitation - cannot be fixed"`
- `"Intentional design choice - different UIs have different keys"`
- `"Feature request, not a bug - would require new implementation"`
- `"Documentation-only issue - should be in docs-v14.md"`

## Ignore File Format

`.consistency_ignore.json`:
```json
{
  "_comment": "Issues marked as reviewed/ignored",
  "ignored_issues": {
    "abc123def456": {
      "description": "SandboxedFileIO methods documented as STUB",
      "reason": "Already verified - documentation correct",
      "reviewed_by": "human",
      "reviewed_date": "2025-11-09",
      "files": ["src/file_io.py"]
    }
  }
}
```

## Re-enabling an Issue

To un-ignore an issue, edit `.consistency_ignore.json` and remove its entry, or delete the entire file to reset.

## What Gets Filtered

Both types of issues are filtered:
- **Code vs Comment Conflicts** (code_conflicts)
- **General Inconsistencies** (all_inconsistencies)

The filter matches on:
- Issue description (case-insensitive, normalized)
- Affected files (sorted list)

## Report Output

When issues are filtered, the report shows:
```
**Note:** 10 issue(s) suppressed (marked as reviewed/ignored)
- See `.consistency_ignore.json` for details
- Use `utils/checker/mark_ignored.py` to manage ignored issues
```

## Tips

1. **Be specific with reasons** - Future you will thank you
2. **Review periodically** - Some ignored issues may become relevant again after code changes
3. **Don't ignore real bugs** - Only ignore false positives, platform limitations, or documented design choices
4. **Use interactive mode** - It's easier than editing JSON manually
