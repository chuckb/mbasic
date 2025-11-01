#!/usr/bin/env python3
"""
Test that Ctrl+C exits cleanly without error messages.
"""

import pexpect
import sys
import time

def test_ctrl_c_exit():
    """Test that Ctrl+C exits without errors."""
    print("=== Testing Ctrl+C Exit ===\n")

    child = pexpect.spawn(
        'python3 mbasic.py --ui curses',
        encoding='utf-8',
        timeout=10,
        dimensions=(24, 80)
    )

    try:
        # Wait for startup
        print("Starting curses UI...")
        time.sleep(1)

        # Send Ctrl+C
        print("Sending Ctrl+C...")
        child.send('\x03')
        time.sleep(1)

        # Check exit
        if child.isalive():
            print("✗ Process did not exit")
            child.terminate()
            return False
        else:
            print("✓ Process exited cleanly")

        # Check for any error output
        try:
            output = child.before
            if output and ('error' in output.lower() or 'exception' in output.lower() or 'traceback' in output.lower()):
                print(f"✗ Error messages detected:\n{output}")
                return False
            else:
                print("✓ No error messages")
        except:
            pass

        return True

    except Exception as e:
        print(f"✗ Exception: {e}")
        if child.isalive():
            child.terminate()
        return False

def test_ctrl_q_exit():
    """Test that Ctrl+Q exits without errors."""
    print("\n=== Testing Ctrl+Q Exit ===\n")

    child = pexpect.spawn(
        'python3 mbasic.py --ui curses',
        encoding='utf-8',
        timeout=10,
        dimensions=(24, 80)
    )

    try:
        # Wait for startup
        print("Starting curses UI...")
        time.sleep(1)

        # Send Ctrl+Q
        print("Sending Ctrl+Q...")
        child.send('\x11')
        time.sleep(1)

        # Check exit
        if child.isalive():
            print("✗ Process did not exit")
            child.terminate()
            return False
        else:
            print("✓ Process exited cleanly")

        # Check for any error output
        try:
            output = child.before
            if output and ('error' in output.lower() or 'exception' in output.lower() or 'traceback' in output.lower()):
                print(f"✗ Error messages detected:\n{output}")
                return False
            else:
                print("✓ No error messages")
        except:
            pass

        return True

    except Exception as e:
        print(f"✗ Exception: {e}")
        if child.isalive():
            child.terminate()
        return False

if __name__ == '__main__':
    print("Testing Curses UI Exit Behavior\n")
    print("="*60)

    test1 = test_ctrl_c_exit()
    test2 = test_ctrl_q_exit()

    print("\n" + "="*60)
    print("Results:")
    print(f"  Ctrl+C exit: {'PASS' if test1 else 'FAIL'}")
    print(f"  Ctrl+Q exit: {'PASS' if test2 else 'FAIL'}")
    print("="*60)

    sys.exit(0 if (test1 and test2) else 1)
