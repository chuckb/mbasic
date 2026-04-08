"""Line-oriented diff for numbered BASIC programs (current vs pending AI result)."""

from __future__ import annotations

from typing import Dict, List


def line_numbered_program_diff(
    current: Dict[int, str], pending: Dict[int, str]
) -> List[str]:
    """Human-readable delta: prefix '-' / '+' on full source lines (by line number)."""
    out: List[str] = []
    for n in sorted(set(current.keys()) | set(pending.keys())):
        a = current.get(n)
        b = pending.get(n)
        if a == b:
            continue
        if a is None:
            out.append(f"+ {b}")
        elif b is None:
            out.append(f"- {a}")
        else:
            out.append(f"- {a}")
            out.append(f"+ {b}")
    return out
