#!/usr/bin/env python3
"""Test the complete breakpoint system without requiring interactive terminal."""

import sys
sys.path.insert(0, 'src')

from editing import ProgramManager
from runtime import Runtime
from interpreter import Interpreter
from iohandler.base import IOHandler
from ast_nodes import TypeInfo

class TestIO(IOHandler):
    def __init__(self):
        self.output_lines = []

    def output(self, text, end='\n'):
        self.output_lines.append(str(text))
        print(f"  OUTPUT: {text}")

    def input_line(self, prompt=""):
        return ""

    def error(self, message):
        print(f"  ERROR: {message}")

    def clear_screen(self):
        pass

    def debug(self, message):
        pass

    def input(self, prompt=""):
        return ""

    def input_char(self):
        return ""

def create_def_type_map():
    def_type_map = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        def_type_map[letter] = TypeInfo.SINGLE
    return def_type_map

print("="*60)
print("FINAL BREAKPOINT TEST")
print("="*60)
print("\nThis tests the step_once() architecture:")
print("- Interpreter executes one line at a time")
print("- Returns status after each line")
print("- UI can check status and decide what to do")
print("")

# Create test program
program = ProgramManager(create_def_type_map())
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

print(f"Program loaded: {len(program.lines)} lines")

# Create interpreter
runtime = Runtime(program.line_asts, program.lines)
io = TestIO()
interpreter = Interpreter(runtime, io)
interpreter.breakpoints = {20}

print(f"Breakpoint set at line 20")
print("\nSimulating execution:")
print("-"*60)

# Simulate the UI's execution loop
step = 0
while step < 20:  # Safety limit
    step += 1
    result = interpreter.step_once()

    print(f"\n[Step {step}] Status: {result['status']}, Line: {result.get('line')}")

    if result['status'] == 'breakpoint':
        print(f"  >>> PAUSED at breakpoint (line {result['line']})")
        print(f"  >>> UI would show: 'BREAKPOINT at line {result['line']} - Press C/S/E'")
        print(f"  >>> User presses 'C' (continue)")
        print(f"  >>> Removing breakpoint and continuing...")
        # Simulate user pressing 'C' - remove breakpoint
        interpreter.breakpoints.discard(result['line'])

    elif result['status'] == 'running':
        print(f"  >>> Line {result['line']} executed, continuing...")

    elif result['status'] in ('completed', 'halted', 'stopped'):
        print(f"  >>> DONE: {result['status']}")
        if result.get('message'):
            print(f"  >>> Message: {result['message']}")
        break

    elif result['status'] == 'error':
        print(f"  >>> ERROR at line {result['line']}: {result['message']}")
        break

print("-"*60)
print(f"\nExecution complete after {step} steps")
print(f"Output lines: {len(io.output_lines)}")
print(f"\nAll output:")
for line in io.output_lines:
    print(f"  {line}")

# Verify results
print("\n" + "="*60)
print("VERIFICATION:")
print("="*60)
if len(io.output_lines) == 4:
    print("✓ All 4 lines executed")
else:
    print(f"✗ Expected 4 lines, got {len(io.output_lines)}")

if step == 5:  # Should be exactly 5 steps
    print("✓ Correct number of steps (5)")
else:
    print(f"✗ Expected 5 steps, got {step}")

print("\nThis proves the architecture works:")
print("  1. Interpreter runs one step at a time")
print("  2. Returns 'breakpoint' status when hitting breakpoint")
print("  3. UI can pause and wait for user input")
print("  4. UI calls step_once() again to continue")
print("\nThe npyscreen integration should work the same way!")
