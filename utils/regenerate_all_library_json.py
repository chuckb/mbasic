#!/usr/bin/env python3
"""
Regenerate library JSON files from all .bas files in basic/ directories.

This script scans all .bas files in basic/<category>/ directories and generates
corresponding JSON metadata files in docs/library/.

Usage:
    python3 utils/regenerate_all_library_json.py
"""

import json
import re
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).parent.parent

# Category metadata
CATEGORY_INFO = {
    "games": {
        "title": "MBASIC Games Library",
        "description": "Classic BASIC games from the CP/M era"
    },
    "utilities": {
        "title": "MBASIC Utilities Library",
        "description": "Utility programs for file management, conversion, and system tools"
    },
    "demos": {
        "title": "MBASIC Demos & Tests",
        "description": "Demonstration programs and test suites"
    },
    "education": {
        "title": "MBASIC Educational Programs",
        "description": "Learning and educational programs"
    },
    "business": {
        "title": "MBASIC Business Programs",
        "description": "Business applications and tools"
    },
    "telecommunications": {
        "title": "MBASIC Telecommunications",
        "description": "Modem, terminal, and BBS programs"
    },
    "electronics": {
        "title": "MBASIC Electronics Programs",
        "description": "Hardware interfacing and electronics tools"
    },
    "data_management": {
        "title": "MBASIC Data Management",
        "description": "Database and file management programs"
    },
    "ham_radio": {
        "title": "MBASIC Ham Radio Programs",
        "description": "Amateur radio utilities and tools"
    },
}


def extract_program_info(filepath: Path) -> Dict:
    """Extract metadata from a BASIC program's header comments."""
    info = {
        "filename": filepath.name,
        "source_path": str(filepath.relative_to(ROOT)),
        "title": filepath.stem.replace("_", " ").title(),
        "description": "",
        "year": "1980s",
        "tags": []
    }

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            # Read first 30 lines to extract metadata
            lines = [f.readline() for _ in range(30)]

            # Look for REMARK/REM lines with metadata
            for line in lines:
                line = line.strip()

                # Extract version/date from first REMARK
                if 'REMARK' in line.upper() or line.upper().startswith('REM '):
                    # Extract program name and version
                    match = re.search(r'(?:REMARK|REM)\s+(.+?)(?:Version|v\.?|$)', line, re.IGNORECASE)
                    if match and not info.get('extracted_title'):
                        title_text = match.group(1).strip()
                        if title_text and len(title_text) < 50:
                            info['extracted_title'] = title_text

                    # Extract year/date
                    date_match = re.search(r'(\d{4})', line)
                    if date_match:
                        year = date_match.group(1)
                        if 1970 <= int(year) <= 1995:
                            info['year'] = year

                    # Extract author
                    if 'by' in line.lower() or 'author' in line.lower():
                        author_match = re.search(r'(?:by|author:?)\s+(.+?)(?:\s+\d{4}|$)', line, re.IGNORECASE)
                        if author_match:
                            info['author'] = author_match.group(1).strip()

                # Extract description from PRINT statements
                if line.upper().startswith('PRINT') and '"' in line:
                    desc_match = re.search(r'PRINT\s+"([^"]+)"', line, re.IGNORECASE)
                    if desc_match:
                        desc = desc_match.group(1).strip()
                        if len(desc) > 20 and not info['description']:
                            info['description'] = desc

    except Exception as e:
        print(f"  ⚠  Warning: Could not read {filepath}: {e}")

    # Use extracted title if better than filename
    if info.get('extracted_title'):
        extracted = info['extracted_title']
        # Only use if it looks like a real title (not just noise)
        if len(extracted) > 3 and not extracted.startswith(':'):
            info['title'] = extracted
        del info['extracted_title']

    # Generate tags based on filename
    filename_lower = filepath.stem.lower()
    if 'test' in filename_lower:
        info['tags'].append('test')

    return info


def generate_category_json(category: str, category_info: Dict):
    """Generate JSON file for a category by scanning its directory."""
    print(f"\n{'='*60}")
    print(f"Processing {category}")
    print(f"{'='*60}")

    # Find all .bas files in the category directory
    category_dir = ROOT / "basic" / category
    if not category_dir.exists():
        print(f"  ⚠  Directory not found: {category_dir}")
        return

    bas_files = sorted(category_dir.glob("*.bas"))
    print(f"  Found {len(bas_files)} .bas files")

    # Extract info for each program
    program_list = []
    for bas_file in bas_files:
        prog_info = extract_program_info(bas_file)
        program_list.append(prog_info)
        print(f"  ✓ {bas_file.name}")

    # Build JSON structure
    json_data = {
        "title": category_info["title"],
        "description": category_info["description"],
        "programs": program_list
    }

    # Write JSON file
    output_path = ROOT / "docs" / "library" / f"{category}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"  ✅ Generated {category}.json with {len(program_list)} programs")


def main():
    print("=" * 60)
    print("Regenerating Library JSON Files")
    print("=" * 60)

    total_programs = 0

    # Generate JSON for each category
    for category, info in CATEGORY_INFO.items():
        generate_category_json(category, info)

        # Count programs
        json_file = ROOT / "docs" / "library" / f"{category}.json"
        if json_file.exists():
            with open(json_file) as f:
                data = json.load(f)
                total_programs += len(data.get("programs", []))

    print("\n" + "=" * 60)
    print(f"✅ Generated JSON for {len(CATEGORY_INFO)} categories")
    print(f"✅ Total programs indexed: {total_programs}")
    print("=" * 60)


if __name__ == "__main__":
    main()
