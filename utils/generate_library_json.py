#!/usr/bin/env python3
"""
Generate library JSON files for all working programs.

Reads test results and extracts program headers to create
metadata JSON files for each category.

Usage:
    python3 utils/generate_library_json.py /tmp/test_final.txt
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List

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
    "bas_tests": {
        "title": "MBASIC Language Tests",
        "description": "Core language feature tests and examples"
    },
    "tests": {
        "title": "MBASIC Interpreter Tests",
        "description": "Interpreter test suite"
    },
    "tests_with_results": {
        "title": "MBASIC Verified Tests",
        "description": "Tests with verified expected results"
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
            # Read first 20 lines to extract metadata
            lines = [f.readline() for _ in range(20)]

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
        print(f"Warning: Could not read {filepath}: {e}")

    # Use extracted title if better than filename
    if info.get('extracted_title'):
        extracted = info['extracted_title']
        # Only use if it looks like a real title (not just noise)
        if len(extracted) > 3 and not extracted.startswith(':'):
            info['title'] = extracted
        del info['extracted_title']

    # Generate tags based on category and filename
    filename_lower = filepath.stem.lower()
    if 'test' in filename_lower:
        info['tags'].append('test')
    if 'game' in filename_lower:
        info['tags'].append('game')

    return info


def parse_test_results(test_file: Path) -> Dict[str, List[str]]:
    """Parse test results to get list of working programs by category."""
    working = {}

    with open(test_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

        # Look for successful programs in RAN TO COMPLETION section
        # Format: ✅ category/filename.bas
        for match in re.finditer(r'✅\s+(\w+)/(\S+\.bas)', content):
            category = match.group(1)
            filename = match.group(2)

            if category not in working:
                working[category] = []
            working[category].append(filename)

    return working


def generate_category_json(category: str, programs: List[str]):
    """Generate JSON file for a category."""
    if category not in CATEGORY_INFO:
        print(f"Skipping unknown category: {category}")
        return

    category_info = CATEGORY_INFO[category]

    # Build program list
    program_list = []
    for prog_name in sorted(programs):
        prog_path = ROOT / "basic" / category / prog_name
        if prog_path.exists():
            prog_info = extract_program_info(prog_path)
            program_list.append(prog_info)

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

    print(f"✅ Generated {category}.json ({len(program_list)} programs)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 utils/generate_library_json.py <test_results.txt>")
        sys.exit(1)

    test_file = Path(sys.argv[1])
    if not test_file.exists():
        print(f"Error: Test results file not found: {test_file}")
        sys.exit(1)

    print("=" * 60)
    print("Generating Library JSON Files")
    print("=" * 60)

    # Parse test results
    print(f"\nParsing test results: {test_file}")
    working_programs = parse_test_results(test_file)

    total_programs = sum(len(progs) for progs in working_programs.values())
    print(f"Found {total_programs} working programs across {len(working_programs)} categories")

    # Generate JSON for each category
    print("\nGenerating JSON files:")
    for category, programs in sorted(working_programs.items()):
        generate_category_json(category, programs)

    print("\n" + "=" * 60)
    print("✅ Library JSON generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
