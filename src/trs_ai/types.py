"""Shared types for TRS-AI generation backends."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GenerationResult:
    """Result of a program generation request."""

    ok: bool
    lines: List[str]
    error: Optional[str] = None


@dataclass
class ExplainResult:
    """Result of AIEXPLAIN (prose, not program lines)."""

    ok: bool
    text: str
    error: Optional[str] = None
