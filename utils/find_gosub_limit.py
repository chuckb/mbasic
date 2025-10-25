#!/usr/bin/env python3
"""
Binary search to find the GOSUB stack limit in MBASIC 5.21
"""

import subprocess
import os

def create_gosub_test(depth, filename):
    """Create a recursive GOSUB test with CRLF line endings"""
    program = f"""10 D=0:M={depth}
20 GOSUB 100
30 PRINT "Max depth:";D
40 END
100 D=D+1
110 IF D>=M THEN RETURN
120 GOSUB 100
130 RETURN
"""
    # Write with CRLF line endings
    with open(filename, 'wb') as f:
        f.write(program.replace('\n', '\r\n').encode('ascii'))

def test_depth(depth):
    """Test a specific GOSUB depth"""
    filename = 'tests/gostmp.bas'
    create_gosub_test(depth, filename)

    try:
        result = subprocess.run(
            ['../utils/mbasic521', 'gostmp.bas'],
            cwd='tests',
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout + result.stderr

        # Check for errors
        if 'out of memory' in output.lower() or 'overflow' in output.lower():
            return False, 'overflow'
        elif f'Max depth: {depth}' in output:
            return True, 'success'
        else:
            return False, 'unknown'

    except subprocess.TimeoutExpired:
        return False, 'timeout'
    except Exception as e:
        return False, f'error: {e}'

def binary_search_limit():
    """Binary search to find the GOSUB stack limit"""
    print("Searching for GOSUB stack limit in MBASIC 5.21...")
    print("=" * 50)

    # Start with a range
    low = 1
    high = 1000
    last_success = 0

    while low <= high:
        mid = (low + high) // 2
        print(f"\nTesting depth {mid}...", end=' ', flush=True)

        success, reason = test_depth(mid)

        if success:
            print(f"✓ SUCCESS")
            last_success = mid
            low = mid + 1
        else:
            print(f"✗ FAILED ({reason})")
            high = mid - 1

    print("\n" + "=" * 50)
    print(f"Maximum GOSUB stack depth: {last_success}")
    print("=" * 50)

    return last_success

if __name__ == '__main__':
    os.chdir('/home/wohl/cl/mbasic')
    limit = binary_search_limit()

    # Create a final test at the limit
    print(f"\nCreating final test file at depth {limit}...")
    create_gosub_test(limit, 'tests/gosubmax.bas')
    print(f"Test file created: tests/gosubmax.bas")
