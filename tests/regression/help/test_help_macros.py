#!/usr/bin/env python3
"""
Test help macro expansion.

Tests that {{kbd:...}} and other macros work correctly.
"""

import sys
import os

# Add project root to path (3 levels up from tests/regression/*/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.ui.help_macros import HelpMacros

def test_curses_macros():
    """Test Curses UI macro expansion."""
    print("Curses UI Macro Test")
    print("=" * 60)
    print()

    help_root = Path(__file__).parent.parent / "docs" / "help"
    macros = HelpMacros('curses', str(help_root))

    test_cases = [
        ("{{kbd:help}}", "Ctrl+H"),
        ("{{kbd:save}}", "Ctrl+V"),  # Curses uses Ctrl+V (Ctrl+S is terminal flow control)
        ("{{kbd:run}}", "Ctrl+R"),
        ("{{kbd:new}}", "Ctrl+N"),
        ("{{kbd:quit}}", "Ctrl+Q"),
        ("{{kbd:toggle_breakpoint}}", "Ctrl+B"),
        ("{{kbd:step}}", "Ctrl+T"),
        ("{{kbd:goto_line}}", "Ctrl+G"),
        ("{{kbd:search}}", "/"),
        ("{{kbd:back}}", "U"),
        ("{{version}}", "5.21"),
        ("{{ui}}", "Curses"),
    ]

    all_passed = True
    for input_text, expected in test_cases:
        result = macros.expand(input_text)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"{status} {input_text:30} → {result:15} (expected: {expected})")

    print()
    return all_passed

def test_tk_macros():
    """Test Tk UI macro expansion."""
    print("Tk UI Macro Test")
    print("=" * 60)
    print()

    help_root = Path(__file__).parent.parent / "docs" / "help"
    macros = HelpMacros('tk', str(help_root))

    test_cases = [
        ("{{kbd:help_topics}}", "Ctrl+?"),
        ("{{kbd:file_new}}", "Ctrl+N"),
        ("{{kbd:file_save}}", "Ctrl+S"),
        ("{{kbd:run_program}}", "Ctrl+R"),  # Updated from F5 to Ctrl+R
        ("{{version}}", "5.21"),
        ("{{ui}}", "Tk"),
    ]

    all_passed = True
    for input_text, expected in test_cases:
        result = macros.expand(input_text)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"{status} {input_text:30} → {result:15} (expected: {expected})")

    print()
    return all_passed

def test_markdown_context():
    """Test macros in actual markdown context."""
    print("Markdown Context Test")
    print("=" * 60)
    print()

    help_root = Path(__file__).parent.parent / "docs" / "help"
    macros = HelpMacros('curses', str(help_root))

    markdown = """
Press **{{kbd:help}}** to open help.
Use **{{kbd:save}}** to save your program.
Version {{version}} of {{ui}}.
"""

    expected = """
Press **Ctrl+H** to open help.
Use **Ctrl+V** to save your program.
Version 5.21 of Curses.
"""

    result = macros.expand(markdown)
    passed = result == expected

    if passed:
        print("✓ Markdown expansion works correctly")
    else:
        print("✗ Markdown expansion failed")
        print("\nExpected:")
        print(expected)
        print("\nGot:")
        print(result)

    print()
    return passed

def test_cross_ui_macros():
    """Test cross-UI macro expansion."""
    print("Cross-UI Macro Test")
    print("=" * 60)
    print()

    help_root = Path(__file__).parent.parent / "docs" / "help"
    # Use any UI, doesn't matter since we're specifying UIs in macros
    macros = HelpMacros('curses', str(help_root))

    test_cases = [
        # Cross-UI lookups - use correct action names for each UI
        ("{{kbd:save:curses}}", "Ctrl+V"),  # Curses uses 'save'
        ("{{kbd:file_save:tk}}", "Ctrl+S"),  # Tk uses 'file_save'
        ("{{kbd:run:curses}}", "Ctrl+R"),  # Curses uses 'run'
        ("{{kbd:run_program:tk}}", "Ctrl+R"),  # Tk uses 'run_program'
        ("{{kbd:help:curses}}", "Ctrl+H"),  # Curses uses 'help'
        ("{{kbd:help_topics:tk}}", "Ctrl+?"),  # Tk uses 'help_topics'
        ("{{kbd:new:curses}}", "Ctrl+N"),  # Curses uses 'new'
        ("{{kbd:file_new:tk}}", "Ctrl+N"),  # Tk uses 'file_new'
        ("{{kbd:toggle_variables:tk}}", "Ctrl+W"),  # Tk-specific
        ("{{kbd:toggle_breakpoint:curses}}", "Ctrl+B"),  # Both have this
        ("{{kbd:toggle_breakpoint:tk}}", "Ctrl+B"),  # Both have this
        # CLI lookups
        ("{{kbd:run:cli}}", "RUN"),  # CLI uses commands
        ("{{kbd:save:cli}}", "SAVE \"file\""),
        ("{{kbd:new:cli}}", "NEW"),
        ("{{kbd:help:cli}}", "HELP"),
        ("{{kbd:stop:cli}}", "Ctrl+C"),
        ("{{kbd:step:cli}}", "STEP"),
        # Web lookups
        ("{{kbd:run:web}}", "Ctrl+R/F5"),  # Web uses keyboard shortcuts
        ("{{kbd:save:web}}", "Ctrl+S"),
        ("{{kbd:new:web}}", "Ctrl+N"),
        ("{{kbd:help:web}}", "F1"),
        ("{{kbd:stop:web}}", "Esc"),
        ("{{kbd:toggle_breakpoint:web}}", "F9"),
        ("{{kbd:step:web}}", "F10"),
    ]

    all_passed = True
    for input_text, expected in test_cases:
        result = macros.expand(input_text)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"{status} {input_text:30} → {result:15} (expected: {expected})")

    print()
    return all_passed

if __name__ == '__main__':
    print("MBASIC Help Macro Test")
    print()

    success = True

    # Test 1: Curses macros
    if not test_curses_macros():
        success = False

    # Test 2: Tk macros
    if not test_tk_macros():
        success = False

    # Test 3: Markdown context
    if not test_markdown_context():
        success = False

    # Test 4: Cross-UI macros
    if not test_cross_ui_macros():
        success = False

    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
