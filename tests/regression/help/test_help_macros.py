#!/usr/bin/env python3
"""
Test help macro expansion.

Tests that {{kbd:...}} and other macros work correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ui.help_macros import HelpMacros

def test_curses_macros():
    """Test Curses UI macro expansion."""
    print("Curses UI Macro Test")
    print("=" * 60)
    print()

    help_root = Path(__file__).parent.parent / "docs" / "help"
    macros = HelpMacros('curses', str(help_root))

    test_cases = [
        ("{{kbd:help}}", "Ctrl+H"),
        ("{{kbd:save}}", "Ctrl+S"),
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
        ("{{kbd:run_program}}", "F5"),
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
Use **Ctrl+S** to save your program.
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

    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
