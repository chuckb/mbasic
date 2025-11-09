#!/usr/bin/env python3
"""
Compute stable hashes for consistency issues.

The hash is based on STABLE data that doesn't change between runs:
- Affected file paths (sorted)
- First 200 chars of Details field (actual code/comments, not Claude's description)
- Issue type (if available)

This ensures the same underlying issue gets the same hash even if Claude
describes it differently on each run.
"""

import hashlib
import re


def normalize_details(details: str, max_chars: int = 200) -> str:
    """Normalize details text for stable hashing.

    Args:
        details: The details text (code snippets, comments, etc.)
        max_chars: Maximum characters to use for hashing

    Returns:
        Normalized text for hashing
    """
    if not details:
        return ""

    # Remove Claude's analysis comments that vary between runs
    # Keep only the actual code/comment text

    # Common patterns to remove:
    # "This is a significant behavior..."
    # "This means..."
    # "The inconsistency:"
    # "However,"

    # Take first section before any analysis
    # Usually the actual code/comment comes first

    # Split by common analysis markers
    analysis_markers = [
        "This is a significant",
        "This means",
        "The inconsistency:",
        "However,",
        "This comment",
        "This creates",
        "This is a design",
    ]

    lines = details.split('\n')
    cleaned_lines = []

    for line in lines:
        # Stop at analysis markers
        if any(marker in line for marker in analysis_markers):
            break
        cleaned_lines.append(line)

    cleaned = '\n'.join(cleaned_lines)

    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # Take first N characters
    return cleaned[:max_chars].lower()


def compute_stable_hash(files: list, details: str = "", issue_type: str = "") -> str:
    """Compute a stable hash for an issue.

    Args:
        files: List of affected file paths
        details: Details text (code snippets, comments)
        issue_type: Type of issue (e.g., "code_vs_comment")

    Returns:
        12-character hash
    """
    # Sort files for consistency
    sorted_files = sorted(files) if files else []

    # Normalize details
    norm_details = normalize_details(details)

    # Build hash input from stable parts
    parts = []

    # Files are the most stable identifier
    parts.append("||".join(sorted_files))

    # Type helps distinguish different issues in same file
    if issue_type:
        parts.append(issue_type.lower().strip())

    # Details anchor to specific code/comment
    if norm_details:
        parts.append(norm_details)

    # Combine parts
    hash_input = "::".join(parts)

    # Compute hash
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()[:12]


def compute_legacy_hash(description: str, files: list) -> str:
    """Compute hash the old way (for migration).

    This is kept for backward compatibility.
    """
    normalized = description.lower().strip() + "||" + "||".join(sorted(files))
    return hashlib.md5(normalized.encode()).hexdigest()[:12]


# Test
if __name__ == '__main__':
    # Test case 1: Same details, different description
    files1 = ['src/file_io.py']
    details1 = '''Class docstring says:
"Implementation status:
- list_files(): IMPLEMENTED - delegates to backend.sandboxed_fs
- load_file(): STUB - raises IOError"'''

    desc1 = "SandboxedFileIO methods documented as STUB but implementation status unclear"
    desc2 = "SandboxedFileIO methods documented as STUB but list_files() is IMPLEMENTED"

    hash1 = compute_stable_hash(files1, details1, "Code vs Documentation")
    hash2 = compute_stable_hash(files1, details1, "Code vs Documentation")

    legacy1 = compute_legacy_hash(desc1, files1)
    legacy2 = compute_legacy_hash(desc2, files1)

    print("Test: Same details, different descriptions")
    print(f"  New hash (desc1): {hash1}")
    print(f"  New hash (desc2): {hash2}")
    print(f"  Match: {hash1 == hash2} ✓" if hash1 == hash2 else f"  Match: {hash1 == hash2} ✗")
    print()
    print(f"  Legacy hash (desc1): {legacy1}")
    print(f"  Legacy hash (desc2): {legacy2}")
    print(f"  Match: {legacy1 == legacy2} ✓" if legacy1 == legacy2 else f"  Match: {legacy1 == legacy2} ✗")
    print()

    # Test case 2: Different files
    files2 = ['src/file_io.py', 'src/editing/manager.py']
    hash3 = compute_stable_hash(files2, details1, "Code vs Documentation")
    print("Test: Different files, same details")
    print(f"  Hash (1 file):  {hash1}")
    print(f"  Hash (2 files): {hash3}")
    print(f"  Different: {hash1 != hash3} ✓" if hash1 != hash3 else f"  Different: {hash1 != hash3} ✗")
