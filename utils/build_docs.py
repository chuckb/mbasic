#!/usr/bin/env python3
"""
Build MBASIC Documentation

This script coordinates all documentation build tasks:
1. Help system indexes (merging + validation)
2. Library documentation (games, examples)
3. Web documentation compilation (MkDocs)

Usage:
    python3 utils/build_docs.py [--help-only] [--web-only] [--validate-only]

Exit codes:
    0 - Success
    1 - Build errors
"""

import sys
import subprocess
from pathlib import Path
from typing import List


class DocBuilder:
    """Coordinates all documentation build tasks."""

    def __init__(self, root_dir: Path):
        """
        Initialize the builder.

        Args:
            root_dir: Project root directory
        """
        self.root_dir = root_dir
        self.utils_dir = root_dir / 'utils'
        self.docs_dir = root_dir / 'docs'
        self.errors: List[str] = []

    def run_command(self, cmd: List[str], description: str) -> bool:
        """
        Run a subprocess command.

        Args:
            cmd: Command to run as list
            description: Description for user

        Returns:
            True if successful
        """
        print(f"\n{'='*70}")
        print(f"  {description}")
        print(f"{'='*70}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.root_dir,
                capture_output=False,
                text=True
            )

            if result.returncode != 0:
                self.errors.append(f"{description} failed with exit code {result.returncode}")
                return False

            return True

        except FileNotFoundError:
            self.errors.append(f"Command not found: {cmd[0]}")
            return False
        except Exception as e:
            self.errors.append(f"{description} failed: {e}")
            return False

    def build_help_indexes(self, validate_only: bool = False) -> bool:
        """
        Build help system indexes.

        Args:
            validate_only: Only validate, don't write

        Returns:
            True if successful
        """
        cmd = [sys.executable, str(self.utils_dir / 'build_help_indexes.py')]
        if validate_only:
            cmd.append('--validate-only')

        return self.run_command(cmd, "Building help indexes")

    def build_library_docs(self) -> bool:
        """
        Build library documentation (games, examples, etc.).

        Returns:
            True if successful
        """
        return self.run_command(
            [sys.executable, str(self.utils_dir / 'build_library_docs.py')],
            "Building library documentation"
        )

    def build_web_docs(self) -> bool:
        """
        Build web documentation (MkDocs).

        Returns:
            True if successful
        """
        # Check if mkdocs is available
        mkdocs_yml = self.root_dir / 'mkdocs.yml'

        if not mkdocs_yml.exists():
            print("\n📝 Note: mkdocs.yml not found, skipping web docs build")
            return True

        # Check if mkdocs is installed
        try:
            subprocess.run(
                ['mkdocs', '--version'],
                capture_output=True,
                check=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("\n📝 Note: mkdocs not installed, skipping web docs build")
            print("   Install with: pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin")
            return True

        # Build with mkdocs
        return self.run_command(
            ['mkdocs', 'build', '--strict'],
            "Building web documentation (MkDocs)"
        )

    def build_all(
        self,
        help_only: bool = False,
        web_only: bool = False,
        validate_only: bool = False
    ) -> bool:
        """
        Build all documentation.

        Args:
            help_only: Only build help indexes
            web_only: Only build web docs
            validate_only: Only validate, don't write

        Returns:
            True if successful
        """
        success = True

        # Build help indexes (unless web-only)
        if not web_only:
            if not self.build_help_indexes(validate_only):
                success = False

        # Build library docs (unless help-only or validate-only)
        if not help_only and not validate_only:
            if not self.build_library_docs():
                success = False

        # Build web docs (unless help-only or validate-only)
        if not help_only and not validate_only:
            if not self.build_web_docs():
                success = False

        # Print summary
        print(f"\n{'='*70}")
        print("  BUILD SUMMARY")
        print(f"{'='*70}")

        if self.errors:
            print(f"\n❌ BUILD FAILED ({len(self.errors)} errors):")
            for error in self.errors:
                print(f"  • {error}")
            return False
        else:
            print("\n✅ ALL DOCUMENTATION BUILT SUCCESSFULLY")
            return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Build all MBASIC documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 utils/build_docs.py                    # Build everything
  python3 utils/build_docs.py --help-only       # Only build help indexes
  python3 utils/build_docs.py --web-only        # Only build web docs
  python3 utils/build_docs.py --validate-only   # Validate help without writing
        """
    )

    parser.add_argument(
        '--help-only',
        action='store_true',
        help='Only build help indexes'
    )
    parser.add_argument(
        '--web-only',
        action='store_true',
        help='Only build web documentation'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate help indexes, do not write'
    )

    args = parser.parse_args()

    # Find project root
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    # Build
    builder = DocBuilder(root_dir)
    success = builder.build_all(
        help_only=args.help_only,
        web_only=args.web_only,
        validate_only=args.validate_only
    )

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
