"""UI backends for MBASIC interpreter.

This module provides abstract interfaces and implementations for different
UI types (CLI, GUI, web, mobile, etc.).
"""

from .base import UIBackend

__all__ = ['UIBackend']
