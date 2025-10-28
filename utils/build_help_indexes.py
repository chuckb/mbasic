#!/usr/bin/env python3
"""
Build Help Indexes for MBASIC UIs

This script merges the three-tier help system (language + mbasic + ui-specific)
into a single pre-built index per UI. This catches broken links at build time
instead of runtime, improving reliability.

Usage:
    python3 utils/build_help_indexes.py [--validate-only]

Outputs:
    - docs/help/ui/tk/merged_index.json
    - docs/help/ui/curses/merged_index.json
    - docs/help/ui/web/merged_index.json (future)

Exit codes:
    0 - Success
    1 - Validation errors found
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re

# Add src directory to Python path for importing HelpMacros
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from ui.help_macros import HelpMacros


class HelpIndexBuilder:
    """Builds and validates merged help indexes for each UI."""

    def __init__(self, help_root: Path):
        """
        Initialize the builder.

        Args:
            help_root: Path to docs/help directory
        """
        self.help_root = help_root
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def load_index(self, index_path: Path) -> Dict:
        """
        Load a search index file.

        Args:
            index_path: Path to search_index.json

        Returns:
            Loaded index dict or empty dict if not found
        """
        if not index_path.exists():
            self.errors.append(f"Index not found: {index_path}")
            return {"files": []}

        try:
            with open(index_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in {index_path}: {e}")
            return {"files": []}
        except Exception as e:
            self.errors.append(f"Error loading {index_path}: {e}")
            return {"files": []}

    def validate_file_exists(self, relative_path: str, base_dir: Path) -> bool:
        """
        Validate that a help file exists.

        Args:
            relative_path: Path relative to base_dir (e.g., "statements/print.md")
            base_dir: Base directory (e.g., docs/help/common/language)

        Returns:
            True if file exists
        """
        full_path = base_dir / relative_path
        if not full_path.exists():
            self.errors.append(f"Help file not found: {full_path}")
            return False
        return True

    def extract_links_from_markdown(self, file_path: Path) -> List[str]:
        """
        Extract all markdown links from a file.

        Args:
            file_path: Path to markdown file

        Returns:
            List of link targets (the URL part of [text](url))
        """
        links = []
        try:
            content = file_path.read_text(encoding='utf-8')

            # Find all [text](url) patterns
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            for match in re.finditer(link_pattern, content):
                url = match.group(2)
                # Skip external links (http://, https://, mailto:)
                if not url.startswith(('http://', 'https://', 'mailto:', '#')):
                    links.append(url)

        except Exception as e:
            self.warnings.append(f"Error reading {file_path} for link extraction: {e}")

        return links

    def validate_link(self, link: str, source_file: Path) -> bool:
        """
        Validate that a link target exists.

        Args:
            link: Link URL (e.g., "../statements/print.md" or "common/language/...")
            source_file: Source file containing the link

        Returns:
            True if link target exists
        """
        # Strip anchor fragments (#section) - we only validate file existence
        link_without_anchor = link.split('#')[0]

        # Skip empty links (pure anchors like "#section")
        if not link_without_anchor:
            return True

        # Resolve link relative to source file's directory
        if link_without_anchor.startswith('common/') or link_without_anchor.startswith('/common/'):
            # Absolute path from help root
            target = self.help_root / link_without_anchor.lstrip('/')
        else:
            # Relative path from source file
            target = (source_file.parent / link_without_anchor).resolve()

        if not target.exists():
            self.errors.append(f"Broken link in {source_file.relative_to(self.help_root)}: {link} -> {target}")
            return False

        return True

    def validate_macros_in_file(self, file_path: Path):
        """
        Validate that all macros can be expanded in a markdown file.

        Args:
            file_path: Path to markdown file
        """
        try:
            content = file_path.read_text(encoding='utf-8')

            # Try to expand macros using the current UI's macro expander
            if hasattr(self, 'macro_expander'):
                expanded = self.macro_expander.expand(content)
            else:
                expanded = content

            # Find any remaining unexpanded macro patterns like {{kbd:...}} or {{...}}
            macro_pattern = r'\{\{[^}]+\}\}'

            for line_num, line in enumerate(expanded.split('\n'), 1):
                for match in re.finditer(macro_pattern, line):
                    macro = match.group(0)
                    self.errors.append(
                        f"Unexpanded macro in {file_path.relative_to(self.help_root)}:{line_num}: {macro}"
                    )

        except Exception as e:
            self.warnings.append(f"Error reading {file_path} for macro validation: {e}")

    def validate_all_links_in_file(self, file_path: Path):
        """
        Validate all links in a markdown file.

        Args:
            file_path: Path to markdown file
        """
        links = self.extract_links_from_markdown(file_path)
        for link in links:
            self.validate_link(link, file_path)

    def merge_indexes_for_ui(self, ui_name: str) -> Dict:
        """
        Merge language + mbasic + ui-specific indexes for a UI.

        Args:
            ui_name: UI name ('tk', 'curses', or 'web')

        Returns:
            Merged index dict
        """
        print(f"\n{'='*60}")
        print(f"Building help index for: {ui_name}")
        print(f"{'='*60}")

        # Create macro expander for this UI
        self.macro_expander = HelpMacros(ui_name, str(self.help_root))

        # Load the three tiers
        language_index = self.load_index(self.help_root / 'common/language/search_index.json')
        mbasic_index = self.load_index(self.help_root / 'mbasic/search_index.json')
        ui_index = self.load_index(self.help_root / f'ui/{ui_name}/search_index.json')

        # Track paths we've seen to detect duplicates
        seen_paths: Set[str] = set()
        merged_files = []

        # Helper to add files with base directory prefix
        def add_files(files: List[Dict], base_dir: str, tier_name: str):
            for file_entry in files:
                # Make path absolute from help root
                if base_dir:
                    full_path = f"{base_dir}/{file_entry['path']}"
                else:
                    full_path = file_entry['path']

                # Check for duplicates
                if full_path in seen_paths:
                    self.warnings.append(f"Duplicate path in {tier_name}: {full_path}")
                    continue

                seen_paths.add(full_path)

                # Add tier information
                entry = file_entry.copy()
                entry['path'] = full_path
                entry['tier'] = tier_name
                merged_files.append(entry)

                # Validate file exists
                file_path = self.help_root / full_path
                if self.validate_file_exists(full_path, self.help_root):
                    # Validate all links in the file
                    self.validate_all_links_in_file(file_path)
                    # Validate no unexpanded macros
                    self.validate_macros_in_file(file_path)

        # Merge in order: language, mbasic, ui-specific
        add_files(language_index.get('files', []), 'common/language', 'language')
        add_files(mbasic_index.get('files', []), 'mbasic', 'mbasic')
        add_files(ui_index.get('files', []), f'ui/{ui_name}', f'ui/{ui_name}')

        print(f"  Language topics: {len(language_index.get('files', []))}")
        print(f"  MBASIC topics:   {len(mbasic_index.get('files', []))}")
        print(f"  UI topics:       {len(ui_index.get('files', []))}")
        print(f"  Total merged:    {len(merged_files)}")

        return {
            'ui': ui_name,
            'generated': 'build_help_indexes.py',
            'files': merged_files
        }

    def write_merged_index(self, ui_name: str, merged_index: Dict):
        """
        Write merged index to output file.

        Args:
            ui_name: UI name ('tk', 'curses', 'web')
            merged_index: Merged index dict
        """
        output_path = self.help_root / f'ui/{ui_name}/merged_index.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_path, 'w') as f:
                json.dump(merged_index, f, indent=2)
            print(f"  ✓ Written: {output_path}")
        except Exception as e:
            self.errors.append(f"Error writing {output_path}: {e}")

    def build_all(self, validate_only: bool = False) -> bool:
        """
        Build indexes for all UIs.

        Args:
            validate_only: If True, only validate without writing

        Returns:
            True if successful (no errors)
        """
        uis = ['tk', 'curses']  # Web UI doesn't have search yet

        for ui in uis:
            merged = self.merge_indexes_for_ui(ui)

            if not validate_only:
                self.write_merged_index(ui, merged)

        # Print summary
        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")

        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
            print("\n❌ BUILD FAILED - Fix errors above")
            return False
        else:
            print(f"\n✅ BUILD SUCCESSFUL")
            if self.warnings:
                print(f"   ({len(self.warnings)} warnings)")
            return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Build and validate help indexes for MBASIC UIs'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate, do not write output files'
    )

    args = parser.parse_args()

    # Find help root
    script_dir = Path(__file__).parent
    help_root = script_dir.parent / 'docs' / 'help'

    if not help_root.exists():
        print(f"Error: Help directory not found: {help_root}")
        return 1

    # Build indexes
    builder = HelpIndexBuilder(help_root)
    success = builder.build_all(validate_only=args.validate_only)

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
