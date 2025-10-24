#!/usr/bin/env python3
"""Test breakpoints programmatically without the IDE."""

import sys
import os

# Set debug flag
os.environ['DEBUG_BP'] = '1'

# Add src to path
sys.path.insert(0, 'src')

from editing import ProgramManager
from runtime import Runtime
from interpreter import Interpreter
from iohandler.base import IOHandler
from ast_nodes import TypeInfo

# Simple IO handler
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
print("PROGRAMMATIC BREAKPOINT TEST")
print("="*60)

program = ProgramManager(create_def_type_map())

# Add test program lines
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
        print(f"ERROR parsing line {line_num}: {error}")

print(f"\nProgram loaded with {len(program.lines)} lines")

# Create runtime and IO
runtime = Runtime(program.line_asts, program.lines)
io = SimpleIO()

# Breakpoint callback
breakpoint_hits = []

def bp_callback(line_num, stmt_idx):
    print(f"\n*** BREAKPOINT CALLBACK INVOKED: Line {line_num} ***", file=sys.stderr)
    breakpoint_hits.append(line_num)
    return True  # Continue execution

# Create interpreter with breakpoint callback
interpreter = Interpreter(runtime, io, breakpoint_callback=bp_callback)

# Set breakpoint on line 20
interpreter.breakpoints = {20}

print(f"\nBreakpoints configured: {interpreter.breakpoints}")
print(f"Callback configured: {interpreter.breakpoint_callback is not None}")
print(f"\nRunning program with DEBUG_BP=1...")
print("-"*60)

# Run the program
interpreter.run()

print("-"*60)
print(f"\nExecution complete!")
print(f"Breakpoints hit: {breakpoint_hits}")

if 20 in breakpoint_hits:
    print("\n✓ SUCCESS: Breakpoint on line 20 WAS triggered!")
else:
    print("\n✗ FAILURE: Breakpoint on line 20 was NOT triggered!")
    print("\nThis means the breakpoint system is broken in the interpreter.")

print(f"\nTotal output lines: {len(io.output_lines)}")
