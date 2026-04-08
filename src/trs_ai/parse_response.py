"""Normalize LLM assistant content into numbered BASIC source lines."""

from __future__ import annotations

import json
import re
from typing import List, Optional, Tuple


def strip_markdown_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?\s*", "", t, flags=re.IGNORECASE)
        t = re.sub(r"\s*```\s*$", "", t)
    return t.strip()


def lines_from_parsed_json(data: object) -> Tuple[bool, List[str], Optional[str]]:
    """Extract program lines from a parsed JSON object (AIBASIC contract)."""
    if not isinstance(data, dict):
        return False, [], "AI response JSON must be an object"
    prog = data.get("program")
    if prog is None:
        return False, [], 'AI response JSON missing "program" array'
    if not isinstance(prog, list):
        return False, [], '"program" must be an array of strings'
    out: List[str] = []
    for i, item in enumerate(prog):
        if not isinstance(item, str):
            return False, [], f'"program" entry {i} must be a string'
        line = item.strip()
        if line:
            out.append(line)
    if not out:
        return False, [], '"program" is empty'
    return True, out, None


def parse_assistant_content(content: str) -> Tuple[bool, List[str], Optional[str]]:
    """
    Parse model output into full BASIC lines (each starts with a line number).

    Tries JSON { "dialect", "program": [...] } first, then plain numbered lines.
    """
    raw = strip_markdown_fences(content)
    if not raw:
        return False, [], "Empty AI response"

    try:
        data = json.loads(raw)
        ok, lines, err = lines_from_parsed_json(data)
        if ok:
            return True, lines, None
    except json.JSONDecodeError:
        pass

    lines: List[str] = []
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.match(r"^\d+\s", s):
            lines.append(s)
    if lines:
        return True, lines, None
    return False, [], "No numbered BASIC lines or valid JSON program in AI response"


def parse_explanation_content(content: str) -> Tuple[bool, str, Optional[str]]:
    """Parse model output for AIEXPLAIN: prefer JSON {{\"explanation\": \"...\"}}, else plain text."""
    raw = strip_markdown_fences(content)
    if not raw:
        return False, "", "Empty AI response"

    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            exp = data.get("explanation")
            if isinstance(exp, str) and exp.strip():
                return True, exp.strip(), None
    except json.JSONDecodeError:
        pass

    if raw.strip():
        return True, raw.strip(), None
    return False, "", "Empty explanation"
