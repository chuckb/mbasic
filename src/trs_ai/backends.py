"""Program generation backends (fixture + OpenAI-compatible HTTP)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Optional, Protocol

from src.trs_ai.parse_response import parse_assistant_content
from src.trs_ai.types import GenerationResult


class ProgramGeneratorBackend(Protocol):
    def generate(self, prompt: str, dialect_spec: str) -> GenerationResult:
        ...


FIXTURE_LINES = [
    '10 PRINT "AILOAD_OK"',
    "20 END",
]

# Production system prompt for RemoteChatBackend only (OpenAI-compatible chat API).
# FixtureBackend does not use this string. There is no separate "golden prompt" repo file;
# unit tests pass canned JSON/HTTP bodies in tests/regression/ai/.
#
# Vocabulary is summarized from MBASIC help: docs/help/common/language/statements|functions
# and docs/help/mbasic/features.md (MBASIC 5.21 / BASIC-80).

SYSTEM_PROMPT_TEMPLATE = """You are a code generator for MBASIC 5.21 / Microsoft BASIC-80 as implemented in MBASIC-2025.

Output rules:
- Reply with ONLY one JSON object. No markdown code fences, no prose before or after.
- Schema: {{"dialect": "<string>", "program": ["<line>", ...]}}
- Each "program" entry must be one complete source line starting with a line number (e.g. 10 PRINT \\"HELLO\\").
- Use double quotes for strings; escape internal quotes as \\".
- Keep programs small unless the user asks otherwise.

Language (statements and commands — use valid MBASIC 5.21 syntax only):
AUTO, CALL, CHAIN, CLEAR, CLOAD, CLOSE, COMMON, CONT, CSAVE, DATA, DEF FN, DEFINT, DEFSNG, DEFDBL, DEFSTR, DELETE, DIM, EDIT, END, ERASE, ERROR, FIELD, FILES, FOR, NEXT, GET, GOSUB, RETURN, GOTO, IF, THEN, ELSE, INPUT, INPUT#, LINE INPUT, LINE INPUT#, KILL, LET, LIST, LLIST, LOAD, LPRINT, MERGE, MID$ (assignment form), NAME, NEW, ON ERROR GOTO, ON...GOSUB, ON...GOTO, OPEN, OPTION BASE, OUT, POKE, PRINT, PRINT#, PRINT USING, PUT, RANDOMIZE, READ, REM, RENUM, RESET, RESTORE, RESUME, LSET, RSET, SAVE, STOP, SWAP, TRON, TROFF, WAIT, WHILE, WEND, WIDTH, WRITE, WRITE#
Also available in this implementation (settings / help — avoid in games unless asked): LIMITS, SHOW SETTINGS, SET SETTING, HELP.
Do not use DEF USR (not implemented). Prefer executable program code; for games and utilities avoid LIST, NEW, LOAD, SAVE, AUTO, EDIT, DELETE, RENUM, SYSTEM unless the user explicitly wants session or disk behavior.

Intrinsic functions (may appear in expressions):
ABS, ASC, ATN, CDBL, CHR$, CINT, COS, CSNG, CVD, CVI, CVS, EOF, EXP, FIX, FRE, HEX$, INKEY$, INP, INPUT$, INSTR, INT, LEFT$, LEN, LOC, LOF, LOG, LPOS, MID$, MKD$, MKI$, MKS$, OCT$, PEEK, POS, RIGHT$, RND, SGN, SIN, SPACE$, SPC, SQR, STR$, STRING$, TAB, TAN, USR, VAL, VARPTR

Types and variables: integer %, single !, double #, string $; arrays via DIM; OPTION BASE 0 or 1.

Operators: arithmetic + - * / \\ ^ MOD; relational = <> < > <= >=; logical AND OR NOT XOR EQV IMP; string + for concatenation.

Dialect label for JSON "dialect" field: {dialect}

User request (generate a program):"""


class FixtureBackend:
    """Deterministic program for tests and keyless appliance smoke."""

    def generate(self, prompt: str, dialect_spec: str) -> GenerationResult:
        return GenerationResult(ok=True, lines=list(FIXTURE_LINES))


class RemoteChatBackend:
    """OpenAI-compatible chat completions over HTTPS (stdlib only)."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout_sec: float = 120.0,
    ):
        self.api_key = api_key
        self.base_url = (base_url or os.environ.get("TRS_AI_BASE_URL") or "").strip() or (
            "https://api.openai.com/v1/chat/completions"
        )
        self.model = (model or os.environ.get("TRS_AI_MODEL") or "gpt-4o-mini").strip()
        self.timeout_sec = float(
            os.environ.get("TRS_AI_TIMEOUT_SEC", str(timeout_sec))
        )

    def generate(self, prompt: str, dialect_spec: str) -> GenerationResult:
        system = SYSTEM_PROMPT_TEMPLATE.format(dialect=dialect_spec)
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            self.base_url,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:500]
            return GenerationResult(
                ok=False,
                lines=[],
                error=f"AI HTTP {e.code}: {detail or e.reason}",
            )
        except urllib.error.URLError as e:
            return GenerationResult(ok=False, lines=[], error=f"AI network error: {e.reason}")
        except TimeoutError:
            return GenerationResult(ok=False, lines=[], error="AI request timed out")

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return GenerationResult(ok=False, lines=[], error="AI response was not valid JSON")

        choices = payload.get("choices")
        if not choices or not isinstance(choices, list):
            return GenerationResult(ok=False, lines=[], error="AI response missing choices")
        first = choices[0]
        if not isinstance(first, dict):
            return GenerationResult(ok=False, lines=[], error="AI response malformed choice")
        msg = first.get("message") or {}
        content = msg.get("content") if isinstance(msg, dict) else None
        if not isinstance(content, str):
            return GenerationResult(ok=False, lines=[], error="AI response missing message content")

        ok, lines, err = parse_assistant_content(content)
        if not ok:
            return GenerationResult(ok=False, lines=[], error=err or "Could not parse AI program")
        return GenerationResult(ok=True, lines=lines)


def load_backend_from_env() -> ProgramGeneratorBackend:
    """
    Select backend from environment.

    - TRS_AI_BACKEND=fixture | remote (default: fixture if unset)
    - remote requires TRS_AI_API_KEY
    """
    kind = (os.environ.get("TRS_AI_BACKEND") or "fixture").strip().lower()
    if kind == "remote":
        key = (os.environ.get("TRS_AI_API_KEY") or "").strip()
        if not key:
            return _ErrorBackend("TRS_AI_BACKEND=remote but TRS_AI_API_KEY is not set")
        return RemoteChatBackend(api_key=key)
    if kind == "fixture":
        return FixtureBackend()
    return _ErrorBackend(f"Unknown TRS_AI_BACKEND={kind!r} (use fixture or remote)")


class _ErrorBackend:
    def __init__(self, message: str):
        self._message = message

    def generate(self, prompt: str, dialect_spec: str) -> GenerationResult:
        return GenerationResult(ok=False, lines=[], error=self._message)
