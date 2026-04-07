"""Pytest hooks for regression tests: MBASIC uses split imports (`src.*` + `editing`)."""

import sys
from pathlib import Path

_MBASIC_ROOT = Path(__file__).resolve().parents[2]
_SRC = _MBASIC_ROOT / "src"


def pytest_configure(config):
    # Order matters: package `src` under mbasic root, then flat modules under mbasic/src/
    for p in (_MBASIC_ROOT, _SRC):
        s = str(p)
        if s not in sys.path:
            sys.path.insert(0, s)
