#!/usr/bin/env python3
"""Debug test to see what's happening with breakpoints."""

import sys
sys.path.insert(0, '/home/wohl/cl/mbasic/src')

from editing import ProgramManager
from runtime import Runtime
from interpreter import Interpreter
from iohandler.base import IOHandler

# Create a simple IO handler that prints to console
class DebugIO(IOHandler):
    def output(self, text, end='\n'):
        print(f"OUTPUT: {text}", end=end)

    def input_line(self, prompt=""):
        return ""

    def error(self, message):
        print(f"ERROR: {message}")

# Create test program
program_text = """10 PRINT "Line 10"
20 PRINT "Line 20 - breakpoint here"
30 PRINT "Line 30"
40 PRINT "Line 40"
50 PRINT "Done!"
"""

print("="*60)
print("BREAKPOINT DEBUG TEST")
print("="*60)

# Parse program
from types_def import TypeInfo

def create_default_def_type_map():
    def_type_map = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        def_type_map[letter] = TypeInfo.SINGLE
    return def_type_map

program = ProgramManager(create_default_def_type_map())
for line in program_text.strip().split('\n'):
    parts = line.strip().split(None, 1)
    if parts:
        line_num = int(parts[0])
        full_line = line.strip()
        success, error = program.add_line(line_num, full_line)
        if not success:
            print(f"Parse error on line {line_num}: {error}")

print(f"\nProgram loaded: {len(program.lines)} lines")
print(f"Line ASTs: {len(program.line_asts)}")

# Create runtime and interpreter
runtime = Runtime(program.line_asts, program.lines)
io = DebugIO()

# Breakpoint callback
breakpoint_hit = []
def breakpoint_callback(line_number, stmt_index):
    print(f"\n*** BREAKPOINT HIT at line {line_number} ***")
    breakpoint_hit.append(line_number)
    # Return True to continue
    return True

interpreter = Interpreter(runtime, io, breakpoint_callback=breakpoint_callback)

# Set breakpoint on line 20
interpreter.breakpoints = {20}
print(f"\nBreakpoints set: {interpreter.breakpoints}")

# Run program
print("\nRunning program...")
print("-"*60)
interpreter.run()
print("-"*60)

# Check results
print(f"\nBreakpoints hit: {breakpoint_hit}")
if 20 in breakpoint_hit:
    print("✓ SUCCESS: Breakpoint on line 20 was hit!")
else:
    print("✗ FAILURE: Breakpoint on line 20 was NOT hit!")
    print("\nDebugging info:")
    print(f"  - Breakpoints in interpreter: {interpreter.breakpoints}")
    print(f"  - Callback function: {interpreter.breakpoint_callback}")
    print(f"  - Line table keys: {list(runtime.line_table.keys())}")
