#!/usr/bin/env python3
"""Test the npyscreen-based UI.

NOTE: This must be run in a real terminal, not through automation.
Run: ./test_npyscreen_ui.py
"""

import sys
sys.path.insert(0, 'src')

from editing import ProgramManager
from ui.curses_ui_npy import CursesBackendNpy
from iohandler.base import IOHandler

# Create minimal IO handler
class DummyIO(IOHandler):
    def input(self, prompt=""):
        return ""

    def print(self, *args, **kwargs):
        pass

    def error(self, message):
        pass

    def output(self, text):
        pass

    def input_line(self, prompt=""):
        return ""

    def input_char(self):
        return ""

    def clear_screen(self):
        pass

    def debug(self, message):
        pass

# Create program manager with empty type map
def_type_map = {}
program = ProgramManager(def_type_map)

# Create and start UI
io = DummyIO()
backend = CursesBackendNpy(io, program)
backend.start()
