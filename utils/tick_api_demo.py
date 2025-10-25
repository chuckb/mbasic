#!/usr/bin/env python3
"""
Demo of the tick-based interpreter API for UI integration.

This demonstrates how a GUI framework would use the new API:
- start() to initialize
- tick() to execute quanta of work
- provide_input() when waiting for input
- State inspection and control

This example uses a simple text-based simulation, but the same
pattern works for any event-driven UI framework (Tkinter, Qt, web, etc.)
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from parser import TypeInfo
from runtime import Runtime
from interpreter import Interpreter
from editing import ProgramManager


def create_default_def_type_map():
    """Create default DEF type map (all SINGLE precision)"""
    def_type_map = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        def_type_map[letter] = TypeInfo.SINGLE
    return def_type_map


class SimpleOutputHandler:
    """Simple output handler that just prints"""
    def __init__(self):
        self.outputs = []

    def output(self, text: str, end: str = '\n') -> None:
        print(text, end=end)
        self.outputs.append(text + end)

    def input(self, prompt: str = '') -> str:
        # This should never be called in tick mode!
        raise RuntimeError("input() should not be called in tick mode!")

    def debug(self, text: str) -> None:
        pass


def run_tick_demo():
    """Demonstrate tick-based execution"""

    # Create a simple BASIC program
    program_text = """10 PRINT "Tick-based execution demo"
20 PRINT "This demonstrates non-blocking INPUT"
30 INPUT "Enter your name"; N$
40 INPUT "Enter your age"; A
50 PRINT "Hello "; N$; ", you are "; A; " years old"
60 FOR I = 1 TO 3
70   PRINT "Tick "; I
80 NEXT I
90 PRINT "Program complete!"
100 END
"""

    print("=" * 60)
    print("TICK-BASED INTERPRETER DEMO")
    print("=" * 60)
    print("\nProgram:")
    print(program_text)
    print("\n" + "=" * 60)
    print("EXECUTION (simulating UI event loop):")
    print("=" * 60 + "\n")

    # Write program to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
        f.write(program_text)
        temp_file = f.name

    try:
        # Parse the program using ProgramManager
        def_type_map = create_default_def_type_map()
        program_manager = ProgramManager(def_type_map)
        program_manager.load_from_file(temp_file)

        # Create runtime and interpreter
        runtime = Runtime(program_manager.line_asts)
        io_handler = SimpleOutputHandler()
        interp = Interpreter(runtime, io_handler)
    finally:
        # Clean up temp file
        os.unlink(temp_file)

    # Start execution
    print("[UI] Calling start()")
    state = interp.start()
    print(f"[UI] State: {state.status}")

    # Simulated input queue (in real UI, this would come from user interaction)
    simulated_inputs = ["Alice", "25"]
    input_index = 0

    # Simulate event loop
    tick_count = 0
    while state.status not in ('done', 'error'):
        tick_count += 1

        # Execute one quantum (in real UI, this would be called from timer/idle callback)
        print(f"\n[UI] Tick #{tick_count}: calling tick(max_statements=10)")
        state = interp.tick(mode='run', max_statements=10)
        print(f"[UI] State after tick: {state.status}")

        # Handle state transitions
        if state.status == 'waiting_for_input':
            print(f"[UI] Program is waiting for input")
            print(f"[UI] Prompt: '{state.input_prompt}'")
            print(f"[UI] Variables waiting: {[v.name for v in state.input_variables]}")

            # Simulate getting input from UI (in real UI, this would be from dialog/widget)
            if input_index < len(simulated_inputs):
                user_input = simulated_inputs[input_index]
                input_index += 1
                print(f"[UI] User provided: '{user_input}'")
                print(f"[UI] Calling provide_input('{user_input}')")
                state = interp.provide_input(user_input)
                print(f"[UI] State after provide_input: {state.status}")
            else:
                print("[UI] ERROR: No more simulated inputs!")
                break

        elif state.status == 'at_breakpoint':
            print(f"[UI] Hit breakpoint at line {state.current_line}")
            print(f"[UI] Calling continue_execution()")
            state = interp.continue_execution()

        elif state.status == 'paused':
            print(f"[UI] Program paused at line {state.current_line}")
            print(f"[UI] Calling continue_execution()")
            state = interp.continue_execution()

        # Prevent infinite loop in case of bugs
        if tick_count > 1000:
            print("[UI] ERROR: Too many ticks, aborting!")
            break

    # Final state
    print(f"\n[UI] Final state: {state.status}")
    if state.status == 'error':
        print(f"[UI] Error: {state.error_info.error_message if state.error_info else 'Unknown'}")
    print(f"[UI] Total statements executed: {state.statements_executed}")
    print(f"[UI] Execution time: {state.execution_time_ms:.2f}ms")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


def demo_breakpoint():
    """Demonstrate breakpoint functionality"""

    program_text = """10 PRINT "Start"
20 PRINT "Line 20"
30 PRINT "Line 30 (breakpoint will be here)"
40 PRINT "Line 40"
50 END
"""

    print("\n\n" + "=" * 60)
    print("BREAKPOINT DEMO")
    print("=" * 60)

    # Write program to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
        f.write(program_text)
        temp_file = f.name

    try:
        # Parse
        def_type_map = create_default_def_type_map()
        program_manager = ProgramManager(def_type_map)
        program_manager.load_from_file(temp_file)

        # Create runtime and interpreter
        runtime = Runtime(program_manager.line_asts)
        io_handler = SimpleOutputHandler()
        interp = Interpreter(runtime, io_handler)
    finally:
        os.unlink(temp_file)

    # Set breakpoint
    print("[UI] Setting breakpoint at line 30")
    interp.set_breakpoint(30)

    # Start execution
    state = interp.start()

    tick_count = 0
    while state.status not in ('done', 'error'):
        tick_count += 1
        state = interp.tick(mode='run', max_statements=10)

        if state.status == 'at_breakpoint':
            print(f"\n[UI] HIT BREAKPOINT at line {state.current_line}!")
            print(f"[UI] User can now inspect variables, step through code, etc.")
            print(f"[UI] Resuming execution...")
            state = interp.continue_execution()

        if tick_count > 100:
            break

    print(f"[UI] Program finished")


if __name__ == '__main__':
    run_tick_demo()
    demo_breakpoint()
