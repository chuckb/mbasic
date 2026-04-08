"""Program generation backends (fixture + OpenAI-compatible HTTP)."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Optional, Protocol, Tuple

from src.trs_ai.parse_response import parse_assistant_content, parse_explanation_content
from src.trs_ai.types import ExplainResult, GenerationResult


class ProgramGeneratorBackend(Protocol):
    def generate(self, prompt: str, dialect_spec: str) -> GenerationResult:
        ...

    def merge_program(
        self, existing_source: str, user_prompt: str, dialect_spec: str
    ) -> GenerationResult:
        ...

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
    ) -> GenerationResult:
        ...

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
    ) -> ExplainResult:
        ...


FIXTURE_LINES = [
    '10 PRINT "AILOAD_OK"',
    "20 END",
]

# Production system prompts for RemoteChatBackend only (OpenAI-compatible chat API).
# FixtureBackend does not use these strings. There is no separate "golden prompt" repo file;
# unit tests pass canned JSON/HTTP bodies in tests/regression/ai/.
#
# Vocabulary is summarized from MBASIC help: docs/help/common/language/statements|functions
# and docs/help/mbasic/features.md (MBASIC 5.21 / BASIC-80).

# Shared by generate / merge / fix: what may appear in emitted BASIC lines.
MBASIC_LANGUAGE_RULES = """
Language (statements and commands — use valid MBASIC 5.21 syntax only):
AUTO, CALL, CHAIN, CLEAR, CLOAD, CLOSE, COMMON, CONT, CSAVE, DATA, DEF FN, DEFINT, DEFSNG, DEFDBL, DEFSTR, DELETE, DIM, EDIT, END, ERASE, ERROR, FIELD, FILES, FOR, NEXT, GET, GOSUB, RETURN, GOTO, IF, THEN, ELSE, INPUT, INPUT#, LINE INPUT, LINE INPUT#, KILL, LET, LIST, LLIST, LOAD, LPRINT, MERGE, MID$ (assignment form), NAME, NEW, ON ERROR GOTO, ON...GOSUB, ON...GOTO, OPEN, OPTION BASE, OUT, POKE, PRINT, PRINT#, PRINT USING, PUT, RANDOMIZE, READ, REM, RENUM, RESET, RESTORE, RESUME, LSET, RSET, SAVE, STOP, SWAP, TRON, TROFF, WAIT, WHILE, WEND, WIDTH, WRITE, WRITE#
Also available in this implementation (settings / help — avoid in games unless asked): LIMITS, SHOW SETTINGS, SET SETTING, HELP.
Do not use DEF USR (not implemented). Prefer executable program code; for games and utilities avoid LIST, NEW, LOAD, SAVE, AUTO, EDIT, DELETE, RENUM, SYSTEM unless the user explicitly wants session or disk behavior.

Intrinsic functions (may appear in expressions):
ABS, ASC, ATN, CDBL, CHR$, CINT, COS, CSNG, CVD, CVI, CVS, EOF, EXP, FIX, FRE, HEX$, INKEY$, INP, INPUT$, INSTR, INT, LEFT$, LEN, LOC, LOF, LOG, LPOS, MID$, MKD$, MKI$, MKS$, OCT$, PEEK, POS, RIGHT$, RND, SGN, SIN, SPACE$, SPC, SQR, STR$, STRING$, TAB, TAN, USR, VAL, VARPTR

Types and variables: integer %, single !, double #, string $; arrays via DIM; OPTION BASE 0 or 1.

Operators: arithmetic + - * / \\ ^ MOD; relational = <> < > <= >=; logical AND OR NOT XOR EQV IMP; string + for concatenation.
""".strip()

# Shared JSON contract for any response that returns a full BASIC program as JSON.
JSON_PROGRAM_ENVELOPE_RULES = """Output rules:
- Reply with ONLY one JSON object. No markdown code fences, no prose before or after.
- Schema: {{"dialect": "<string>", "program": ["<line>", ...]}}
- Each "program" entry must be one complete source line starting with a line number (e.g. 10 PRINT \\"HELLO\\").
- Use double quotes for strings; escape internal quotes as \\"."""

JSON_COMPLETE_PROGRAM_RULE = (
    "- Return the COMPLETE program (every numbered line), not a patch or diff."
)


def _system_prompt_generate(dialect: str) -> str:
    return (
        "You are a code generator for MBASIC 5.21 / Microsoft BASIC-80 as implemented in "
        "MBASIC-2025.\n\n"
        f"{JSON_PROGRAM_ENVELOPE_RULES}\n"
        "- Keep programs small unless the user asks otherwise.\n\n"
        f"{MBASIC_LANGUAGE_RULES}\n\n"
        f'Dialect label for JSON "dialect" field: {dialect}\n\n'
        "User request (generate a program):"
    )


def _system_prompt_merge(dialect: str) -> str:
    return (
        "You revise MBASIC 5.21 programs. The user sends the full current program and a "
        "change request.\n\n"
        f"{JSON_PROGRAM_ENVELOPE_RULES}\n"
        f"- {JSON_COMPLETE_PROGRAM_RULE}\n\n"
        f"{MBASIC_LANGUAGE_RULES}\n\n"
        f"Keep the program small unless the user asks otherwise.\n\n"
        f'Dialect label for JSON "dialect" field: {dialect}'
    )


def _system_prompt_fix(dialect: str) -> str:
    return (
        "You fix MBASIC 5.21 programs. The user sends the full program, optional runtime "
        "error context, and an optional hint.\n\n"
        f"{JSON_PROGRAM_ENVELOPE_RULES}\n"
        f"- {JSON_COMPLETE_PROGRAM_RULE}\n\n"
        f"{MBASIC_LANGUAGE_RULES}\n\n"
        f'Dialect label for JSON "dialect" field: {dialect}'
    )


EXPLAIN_SYSTEM = (
    "You explain MBASIC 5.21 (BASIC-80 style) source briefly for a retro BASIC user.\n\n"
    "Output rules:\n"
    '- Reply with ONLY one JSON object: {{"explanation": "<short plain text>"}}\n'
    "- No markdown fences. Keep it concise.\n\n"
    "Reference vocabulary (name statements and functions correctly when explaining):\n"
    + MBASIC_LANGUAGE_RULES
)


def _fixture_next_line_num(source_lines: list[str]) -> int:
    mx = 0
    for raw in source_lines:
        m = re.match(r"^(\d+)\s", raw.strip())
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 10 if mx else 10


class FixtureBackend:
    """Deterministic program for tests and keyless appliance smoke."""

    def generate(self, prompt: str, dialect_spec: str) -> GenerationResult:
        return GenerationResult(ok=True, lines=list(FIXTURE_LINES))

    def merge_program(
        self, existing_source: str, user_prompt: str, dialect_spec: str
    ) -> GenerationResult:
        base = [ln.strip() for ln in existing_source.splitlines() if ln.strip()]
        if not base:
            return GenerationResult(ok=False, lines=[], error="NO PROGRAM IN MEMORY")
        n = _fixture_next_line_num(base)
        snippet = user_prompt.replace("\n", " ")[:60]
        out = base + [f"{n} REM AIMERGE: {snippet}"]
        return GenerationResult(ok=True, lines=out)

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
    ) -> GenerationResult:
        base = [ln.strip() for ln in existing_source.splitlines() if ln.strip()]
        if not base:
            return GenerationResult(ok=False, lines=[], error="NO PROGRAM IN MEMORY")
        n = _fixture_next_line_num(base)
        out = base + [f"{n} REM AIFIX"]
        return GenerationResult(ok=True, lines=out)

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
    ) -> ExplainResult:
        if line_number is not None:
            return ExplainResult(
                ok=True,
                text=f"FIXTURE: Line {line_number} (program {len(existing_source)} chars).",
            )
        return ExplainResult(ok=True, text="FIXTURE: Whole program summary (fixture backend).")


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

    def _post_chat(self, system: str, user: str) -> Tuple[bool, str, Optional[str]]:
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
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
            return False, "", f"AI HTTP {e.code}: {detail or e.reason}"
        except urllib.error.URLError as e:
            return False, "", f"AI network error: {e.reason}"
        except TimeoutError:
            return False, "", "AI request timed out"

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return False, "", "AI response was not valid JSON"

        choices = payload.get("choices")
        if not choices or not isinstance(choices, list):
            return False, "", "AI response missing choices"
        first = choices[0]
        if not isinstance(first, dict):
            return False, "", "AI response malformed choice"
        msg = first.get("message") or {}
        content = msg.get("content") if isinstance(msg, dict) else None
        if not isinstance(content, str):
            return False, "", "AI response missing message content"
        return True, content, None

    def generate(self, prompt: str, dialect_spec: str) -> GenerationResult:
        system = _system_prompt_generate(dialect_spec)
        ok, content, err = self._post_chat(system, prompt)
        if not ok:
            return GenerationResult(ok=False, lines=[], error=err)
        parsed_ok, lines, perr = parse_assistant_content(content)
        if not parsed_ok:
            return GenerationResult(ok=False, lines=[], error=perr or "Could not parse AI program")
        return GenerationResult(ok=True, lines=lines)

    def merge_program(
        self, existing_source: str, user_prompt: str, dialect_spec: str
    ) -> GenerationResult:
        system = _system_prompt_merge(dialect_spec)
        user = (
            f"Current program:\n{existing_source}\n\n"
            f"Modification request:\n{user_prompt}\n"
        )
        ok, content, err = self._post_chat(system, user)
        if not ok:
            return GenerationResult(ok=False, lines=[], error=err)
        parsed_ok, lines, perr = parse_assistant_content(content)
        if not parsed_ok:
            return GenerationResult(ok=False, lines=[], error=perr or "Could not parse AI program")
        return GenerationResult(ok=True, lines=lines)

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
    ) -> GenerationResult:
        system = _system_prompt_fix(dialect_spec)
        err_part = error_context or "(none)"
        hint_part = user_hint or "(none)"
        user = (
            f"Current program:\n{existing_source}\n\n"
            f"Error / failure context:\n{err_part}\n\n"
            f"User hint:\n{hint_part}\n"
        )
        ok, content, err = self._post_chat(system, user)
        if not ok:
            return GenerationResult(ok=False, lines=[], error=err)
        parsed_ok, lines, perr = parse_assistant_content(content)
        if not parsed_ok:
            return GenerationResult(ok=False, lines=[], error=perr or "Could not parse AI program")
        return GenerationResult(ok=True, lines=lines)

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
    ) -> ExplainResult:
        if line_number is not None:
            user = (
                f"Dialect: {dialect_spec}\n"
                f"Focus on line number: {line_number}\n\n"
                f"Program:\n{existing_source}\n"
            )
        else:
            user = f"Dialect: {dialect_spec}\n\nProgram:\n{existing_source}\n"
        ok, content, err = self._post_chat(EXPLAIN_SYSTEM, user)
        if not ok:
            return ExplainResult(ok=False, text="", error=err)
        parsed_ok, text, perr = parse_explanation_content(content)
        if not parsed_ok:
            return ExplainResult(ok=False, text="", error=perr or "Could not parse explanation")
        return ExplainResult(ok=True, text=text)


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

    def merge_program(
        self, existing_source: str, user_prompt: str, dialect_spec: str
    ) -> GenerationResult:
        return GenerationResult(ok=False, lines=[], error=self._message)

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
    ) -> GenerationResult:
        return GenerationResult(ok=False, lines=[], error=self._message)

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
    ) -> ExplainResult:
        return ExplainResult(ok=False, text="", error=self._message)
