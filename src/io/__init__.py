"""I/O abstraction layer for MBASIC interpreter.

This module provides abstract interfaces for I/O operations,
allowing the interpreter to work with different I/O backends
(console, GUI, embedded, etc.).
"""

from .base import IOHandler
from .console import ConsoleIOHandler

__all__ = ['IOHandler', 'ConsoleIOHandler']
