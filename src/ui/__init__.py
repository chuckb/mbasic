"""UI backends for MBASIC interpreter.

This module provides abstract interfaces and implementations for different
UI types (CLI, GUI, web, mobile, etc.).
"""

from .base import UIBackend
from .cli import CLIBackend
from .visual import VisualBackend
from .curses_ui import CursesBackend
from .tk_ui import TkBackend

__all__ = ['UIBackend', 'CLIBackend', 'VisualBackend', 'CursesBackend', 'TkBackend']
