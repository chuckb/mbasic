#!/usr/bin/env python3
"""
Check if all compiler tools (z88dk and tnylpo) are properly installed.

This utility verifies the complete MBASIC compilation toolchain.
"""

import subprocess
import sys
import os

def run_check_script(script_name, tool_name):
    """Run a check script and return success status"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)

    if not os.path.exists(script_path):
        print(f"✗ Check script not found: {script_path}")
        return False

    print(f"\nChecking {tool_name}...")
    print("=" * 60)

    try:
        result = subprocess.run([sys.executable, script_path],
                              capture_output=True,
                              text=True)

        # Check for success markers in output
        if "properly installed and configured" in result.stdout:
            print(f"✓ {tool_name} is properly installed")
            return True
        else:
            print(f"✗ {tool_name} not properly installed")
            print(result.stdout)
            return False

    except Exception as e:
        print(f"✗ Error checking {tool_name}: {e}")
        return False

def main():
    """Check all compiler tools"""
    print("MBASIC Compiler Toolchain Check")
    print("=" * 60)
    print("\nThis utility checks that all required tools are installed:")
    print("1. z88dk - Z80 C compiler (required)")
    print("2. tnylpo - CP/M emulator (optional but recommended)")

    # Check z88dk (required)
    z88dk_ok = run_check_script("check_z88dk.py", "z88dk")

    # Check tnylpo (optional)
    tnylpo_ok = run_check_script("check_tnylpo.py", "tnylpo")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if z88dk_ok:
        print("✓ z88dk compiler: INSTALLED (required)")
    else:
        print("✗ z88dk compiler: NOT FOUND (required)")
        print("  See: docs/dev/COMPILER_SETUP.md")

    if tnylpo_ok:
        print("✓ tnylpo emulator: INSTALLED (optional)")
    else:
        print("⚠ tnylpo emulator: NOT FOUND (optional)")
        print("  See: docs/dev/TNYLPO_SETUP.md")
        print("  Note: tnylpo is only needed to run/test compiled programs")

    print("\n" + "=" * 60)

    if z88dk_ok and tnylpo_ok:
        print("✓ Full toolchain is installed and ready!")
        print("  You can compile and test BASIC programs:")
        print("  python3 test_compile.py program.bas")
        sys.exit(0)
    elif z88dk_ok:
        print("✓ Compiler is ready (can compile but not test)")
        print("  You can compile BASIC programs to .COM files")
        print("  Install tnylpo to test them")
        sys.exit(0)
    else:
        print("✗ Compiler toolchain is not ready")
        print("  Install z88dk first (required)")
        sys.exit(1)

if __name__ == "__main__":
    main()