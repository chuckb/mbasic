#!/usr/bin/env python3
"""Test the step execution without UI."""

import sys
sys.path.insert(0, 'src')

from editing import ProgramManager
from runtime import Runtime
from interpreter import Interpreter
from iohandler.base import IOHandler
from ast_nodes import TypeInfo

class SimpleIO(IOHandler):
    def __init__(self):
        self.output_lines = []

    def output(self, text, end='\n'):
        self.output_lines.append(str(text))
        print(f"OUTPUT: {text}", end=end)

    def input_line(self, prompt=""):
        return ""

    def error(self, message):
        print(f"ERROR: {message}")

    def clear_screen(self):
        pass

    def debug(self, message):
        pass

    def input(self, prompt=""):
        return ""

    def input_char(self):
        return ""

# Create program
def create_def_type_map():
    def_type_map = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        def_type_map[letter] = TypeInfo.SINGLE
    return def_type_map

print("="*60)
print("STEP EXECUTION TEST")
print("="*60)

program = ProgramManager(create_def_type_map())

# Add test program
test_lines = [
    "10 PRINT \"Line 10\"",
    "20 PRINT \"Line 20 - BREAKPOINT\"",
    "30 PRINT \"Line 30\"",
    "40 PRINT \"Line 40\"",
]

for line in test_lines:
    parts = line.split(None, 1)
    line_num = int(parts[0])
    success, error = program.add_line(line_num, line)
    if not success:
        print(f"ERROR: {error}")

print(f"\nProgram loaded: {len(program.lines)} lines")

# Create runtime and interpreter
runtime = Runtime(program.line_asts, program.lines)
io = SimpleIO()
interpreter = Interpreter(runtime, io)

# Set breakpoint on line 20
interpreter.breakpoints = {20}
print(f"Breakpoints set: {interpreter.breakpoints}")

# Step through program
print("\nStepping through program...")
print("-"*60)

step_count = 0
while step_count < 20:  # Safety limit
    step_count += 1
    result = interpreter.step_once()

    print(f"\nStep {step_count}: {result}")

    if result['status'] == 'breakpoint':
        print(f"  *** BREAKPOINT HIT at line {result['line']} ***")
        print(f"  Would show status bar here")
        print(f"  User would press C/S/E")
        print(f"  For this test, we'll 'continue' automatically")
        # Remove breakpoint and continue
        interpreter.breakpoints.discard(result['line'])

    elif result['status'] in ('completed', 'halted', 'stopped', 'error'):
        print(f"  *** EXECUTION ENDED: {result['status']} ***")
        break

print("-"*60)
print(f"\nTotal steps: {step_count}")
print(f"Output lines: {len(io.output_lines)}")

if len(io.output_lines) == 4:
    print("\n✓ SUCCESS: All 4 lines executed")
else:
    print(f"\n✗ FAILURE: Expected 4 lines, got {len(io.output_lines)}")
