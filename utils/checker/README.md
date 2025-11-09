# Documentation Consistency Checker

This directory contains tools for checking consistency between documentation and code.

## Main Scripts

### check_docs_consistency3.py
Enhanced consistency checker that analyzes both code and documentation.

**Features:**
- Analyzes Python source files (.py) and JSON config files (.json)
- Scans documentation files (.md) from docs/help, docs/library, docs/stylesheets, docs/user
- Detects code vs comment conflicts
- Cross-references documentation vs implementation
- **Auto-filters previously reviewed/ignored issues**
- Auto-generates versioned output filenames

**Usage:**
```bash
cd utils/checker
python3 check_docs_consistency3.py
```

**Requirements:**
- pip install anthropic
- ANTHROPIC_API_KEY environment variable

**Output:**
- Saves report to docs/history/docs_inconsistencies_report-vN.md
- Shows how many issues were filtered out as already ignored

### mark_ignored.py
Interactive tool to mark issues as reviewed/ignored.

**Usage:**
```bash
# Mark issues interactively from a report
python3 mark_ignored.py docs/history/code-v14.md

# List all ignored issues
python3 mark_ignored.py --list

# Mark specific issue by hash
python3 mark_ignored.py --hash abc123 --reason "Working as designed"
```

### rebuild_ignore_hashes.py
Utility to rebuild the ignore file with correct hashes.

**When to use:**
- After manually editing .consistency_ignore.json
- If hashes were corrupted or manually created

**Usage:**
```bash
python3 rebuild_ignore_hashes.py
```

Creates backup before rebuilding.

## How the Ignore System Works

1. **Hash Computation**: Each issue gets a unique hash based on:
   - Issue description (normalized to lowercase)
   - Affected file paths (sorted)
   - Format: md5(description.lower() + "||" + "||".join(sorted(files)))[:12]

2. **Filtering**: check_docs_consistency3.py:
   - Loads ignore file at startup
   - Computes hash for each detected issue
   - Filters out issues whose hash matches ignore file
   - Reports how many were filtered

## Troubleshooting

### Problem: Ignore file has 400+ entries but nothing is filtered

**Cause**: The ignore file was created with random/manual hashes instead of computed hashes.

**Solution:**
```bash
python3 rebuild_ignore_hashes.py
```

This happened in v14 - the file had 423 entries, but only 21 were valid (402 had missing data).

### Problem: Verify hash computation is working

**Solution:**
```bash
python3 test_ignore.py
```
