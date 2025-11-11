#!/usr/bin/env python3
"""
Utility to create and verify CP/M text file format.
CP/M text files use:
- CRLF (0x0D 0x0A) for line endings
- ^Z (0x1A) as EOF marker
"""

import sys
import os

def create_cpm_text_file(filename, lines):
    """Create a text file in CP/M format with CRLF and ^Z EOF marker"""
    with open(filename, 'wb') as f:
        for line in lines:
            # Write line with CRLF ending
            f.write(line.encode('ascii'))
            f.write(b'\r\n')  # CRLF
        # Add ^Z EOF marker
        f.write(b'\x1a')
    print(f"Created CP/M format file: {filename}")

def read_cpm_text_file(filename):
    """Read and display a CP/M format text file"""
    with open(filename, 'rb') as f:
        data = f.read()

    print(f"\nReading {filename}:")
    print(f"File size: {len(data)} bytes")
    print("\nHex dump of file:")

    # Show hex dump
    for i in range(0, len(data), 16):
        hex_bytes = ' '.join(f'{b:02x}' for b in data[i:i+16])
        ascii_chars = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        print(f"{i:04x}: {hex_bytes:<48} {ascii_chars}")

    # Show file content as text (stopping at ^Z)
    print("\nText content (until ^Z):")
    text = data.split(b'\x1a')[0]  # Stop at ^Z
    # Replace CRLF with visual marker
    lines = text.split(b'\r\n')
    for i, line in enumerate(lines):
        if line:  # Don't show empty line after last CRLF
            print(f"Line {i+1}: [{line.decode('ascii', errors='replace')}]")

    # Check format
    print("\nFormat analysis:")
    has_crlf = b'\r\n' in data
    has_ctrlz = b'\x1a' in data
    print(f"Has CRLF line endings: {has_crlf}")
    print(f"Has ^Z EOF marker: {has_ctrlz}")

    return has_crlf and has_ctrlz

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Create: python3 cpm_file_format.py create <filename>")
        print("  Read:   python3 cpm_file_format.py read <filename>")
        print("  Test:   python3 cpm_file_format.py test")
        return

    command = sys.argv[1]

    if command == 'create' and len(sys.argv) == 3:
        filename = sys.argv[2]
        # Create a sample CP/M format file
        lines = [
            "This is a CP/M format text file",
            "It has CRLF line endings",
            "And a ^Z EOF marker at the end"
        ]
        create_cpm_text_file(filename, lines)

    elif command == 'read' and len(sys.argv) == 3:
        filename = sys.argv[2]
        if os.path.exists(filename):
            is_cpm = read_cpm_text_file(filename)
            if is_cpm:
                print("\n✓ File is in proper CP/M format")
            else:
                print("\n✗ File is NOT in proper CP/M format")
        else:
            print(f"File not found: {filename}")

    elif command == 'test':
        # Create and verify a test file
        test_file = '/tmp/cpm_test.txt'
        lines = [
            "Test line 1",
            "Test line 2 with data: 123",
            "Test line 3 - final line"
        ]
        create_cpm_text_file(test_file, lines)
        print()
        is_cpm = read_cpm_text_file(test_file)
        if is_cpm:
            print("\n✓ Test passed: CP/M format working correctly")
        else:
            print("\n✗ Test failed: CP/M format not correct")

    else:
        print("Invalid command or arguments")
        print("Use 'create', 'read', or 'test'")

if __name__ == '__main__':
    main()