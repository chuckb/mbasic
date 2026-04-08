"""Program generation backends (fixture + OpenAI-compatible HTTP)."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Optional, Protocol, Tuple

from src.trs_ai.parse_response import parse_explanation_content
from src.trs_ai.types import ExplainResult, GenerationResult
from src.trs_ai.validate_output import (
    ProgramValidationContext,
    extract_program_from_content,
    format_host_diagnostics_for_retry,
    validate_ai_program,
)


def _verbose_section(title: str, body: str) -> None:
    print(f"--- TRS-AI verbose: {title} ---")
    print(body)


def _sorted_numbered_source_lines(source: str) -> list[str]:
    """Strip blanks; sort by BASIC line number; compare full line text (post-strip)."""
    rows: list[tuple[int, str]] = []
    for raw in source.splitlines():
        s = raw.strip()
        if not s:
            continue
        m = re.match(r"^(\d+)\s", s)
        if m:
            rows.append((int(m.group(1)), s))
    rows.sort(key=lambda t: t[0])
    return [t[1] for t in rows]


def merge_output_is_identical_to_base(
    existing_source: str, validated_lines: list[str]
) -> bool:
    """True if merge result is the same program as the input (line numbers + text), ignoring blank lines."""
    a = _sorted_numbered_source_lines(existing_source)
    b = _sorted_numbered_source_lines("\n".join(validated_lines))
    return a == b


_MERGE_IDENTICAL_ERR = (
    "AI MERGE REJECTED: model output is identical to the current program line-for-line "
    "(after host validation repairs). The user asked for a modification — change at least one line: "
    "fix the described bug, add EOF/INPUT# guards, or align PRINT#/LINE INPUT# so save/load use the same "
    "number of lines per record."
)


class ProgramGeneratorBackend(Protocol):
    def generate(
        self,
        prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        ...

    def merge_program(
        self,
        existing_source: str,
        user_prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        ...

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
        *,
        syntax_errors: Optional[str] = None,
        verbose: bool = False,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        ...

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
        verbose: bool = False,
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

# Full vocabulary for AIEXPLAIN only (describing arbitrary user programs).
MBASIC_LANGUAGE_RULES = """
Language (statements and commands — MBASIC 5.21 / BASIC-80 style):
AUTO, CALL, CHAIN, CLEAR, CLOAD, CLOSE, COMMON, CONT, CSAVE, DATA, DEF FN, DEFINT, DEFSNG, DEFDBL, DEFSTR, DELETE, DIM, EDIT, END, ERASE, ERROR, FIELD, FILES, FOR, NEXT, GET, GOSUB, RETURN, GOTO, IF, THEN, ELSE, INPUT, INPUT#, LINE INPUT, LINE INPUT#, KILL, LET, LIST, LLIST, LOAD, LPRINT, MERGE, MID$ (assignment form), NAME, NEW, ON ERROR GOTO, ON...GOSUB, ON...GOTO, OPEN, OPTION BASE, OUT, POKE, PRINT, PRINT#, PRINT USING, PUT, RANDOMIZE, READ, REM, RENUM, RESET, RESTORE, RESUME, LSET, RSET, SAVE, STOP, SWAP, TRON, TROFF, WAIT, WHILE, WEND, WIDTH, WRITE, WRITE#
Also (settings / help): LIMITS, SHOW SETTINGS, SET SETTING, HELP.

Intrinsic functions (expressions): ABS, ASC, ATN, CDBL, CHR$, CINT, COS, CSNG, CVD, CVI, CVS, EOF, EXP, FIX, FRE, HEX$, INKEY$, INP, INPUT$, INSTR, INT, LEFT$, LEN, LOC, LOF, LOG, LPOS, MID$, MKD$, MKI$, MKS$, OCT$, PEEK, POS, RIGHT$, RND, SGN, SIN, SPACE$, SPC, SQR, STR$, STRING$, TAB, TAN, USR, VAL, VARPTR

Types: integer %, single !, double #, string $; DIM arrays; OPTION BASE 0 or 1.
Operators: + - * / \\ ^ MOD; = <> < > <= >=; AND OR NOT XOR EQV IMP; string +.
""".strip()

# Generate / merge / fix only — conservative subset; avoids listing GET/PUT/FIELD that models misapply.
MBASIC_AI_LINE_NUMBER_PLAN = """
Mandatory line-number layout (follow this to avoid duplicate line numbers in one pass):
- 10–89: REM, scalar setup (e.g. COUNT%=0), DIM arrays only. No GOSUB targets here.
- 100–189: Menu loop only (PRINT menu, INPUT choice, IF...THEN GOSUB 200/300/400/500/600, GOTO back to ~100).
- 200–289: First subroutine (e.g. add) through RETURN.
- 300–389: Second subroutine (e.g. load) through RETURN.
- 400–489: Third subroutine (e.g. save) through RETURN.
- 500–589: Fourth subroutine (e.g. search) through RETURN.
- 600–789: Fifth subroutine (e.g. delete) through RETURN.
Use each hundreds block only once; never repeat a line number; never put menu lines and a subroutine in the same block.
""".strip()

MBASIC_AI_GENERATION_RULES = """
You are generating code for the MBASIC-2025 interactive interpreter (strict parser), not for QuickBASIC, QB64, or Visual BASIC.

Safe core statements (representative): REM, LET, DIM (arrays only — see below), END, STOP, PRINT, INPUT,
IF...THEN...ELSE, GOTO, GOSUB, RETURN, FOR...NEXT, WHILE...WEND, ON...GOTO/GOSUB, DATA, READ, RESTORE,
CLEAR, RANDOMIZE, CLOSE, OPEN (see file rules).

DIM rule (parser requirement): DIM only declares arrays with parentheses, e.g. DIM N$(50), A%(10). Never DIM COUNT% or DIM X without ().
Initialize scalars with LET or assignment: COUNT%=0, I=0.

Hard bans (not in this parser or not for AI output): CLS (clear screen), SPLIT, DEF USR.

Sequential disk I/O (use this when the user asks for save/load — do not use random/record APIs):
- OPEN "filename" FOR OUTPUT AS #n — create/overwrite text file.
- OPEN "filename" FOR INPUT AS #n — read existing file.
- OPEN "filename" FOR APPEND AS #n — append (or classic OPEN "O",#n,"f" / OPEN "I",#n,"f" / OPEN "A",#n,"f").
- CLOSE #n when done.

SAVE/LOAD must use the SAME on-disk shape (most common model bug: mismatch → EOF / "Input past end of file"):
- Recommended (clearest): one physical file line per field. SAVE: for each record, use one PRINT # per field
  (e.g. PRINT #1, N$(I) then PRINT #1, E$(I) then …). LOAD: inside WHILE NOT EOF(1), use the same count of
  LINE INPUT #1, var$ in the same order (never fewer or more reads per record than PRINTs per record).
- Alternative: exactly ONE PRINT # line per record (semicolons join all fields on one file line), then exactly
  ONE LINE INPUT #1, R$ per record and split fields with MID$/INSTR (or INPUT #1, a, b, c if types match).
  Do not mix "one PRINT line for the whole record" with "four LINE INPUT lines per record" — that reads past
  the record and fails at EOF.
- Each iteration of a load loop must read a predictable number of lines; if EOF(1) is true before finishing
  those reads, the file was truncated or the format does not match SAVE — fix SAVE or LOAD so counts match.
- Read with LINE INPUT #n, var$ for one string per call (never LINE INPUT #1, A$; B$; C$ — that is invalid).
- Or INPUT #n, vars for simple comma-separated numeric/string fields if you use the same layout with PRINT #.

Hard bans for generated programs (the host rejects these; the model often hallucinates them from other BASICs):
- Never CLS; never SPLIT ... INTO ... (not a statement here — use LINE INPUT # and MID$/INSTR).
- Never OPEN ... FOR RANDOM, FOR BINARY, or any FOR-phrase except INPUT, OUTPUT, APPEND.
- Never OPEN "R", #n, ... (random letter mode).
- Never FIELD #, never GET #n, record, variable$ style (multiple commas after GET/PUT), never PUT #n, record, var$.
- Do not fix file problems by switching to random access — use multiple LINE INPUT # / PRINT # lines and a simple text format instead.
- Do not write one multi-field PRINT # line per record and then read four LINE INPUT # per record (or any unequal count); pair them.

PRINT: prefer semicolons between items. Comma-separated PRINT zones inside long IF...THEN lines often fail parse — split into multiple PRINT lines or use GOSUB.

Types: string $, integer %, single !, double # — keep suffixes consistent. DEF USR is not implemented.

Intrinsic functions (when needed): ABS, ASC, CHR$, CINT, COS, EOF, EXP, INSTR, INT, LEFT$, LEN, MID$, RIGHT$, RND, SGN, SIN, SQR, STR$, VAL, LOF(n) on an open channel, INKEY$, etc. Do not invent functions from other dialects.
""".strip()

# Shared JSON contract for any response that returns a full BASIC program as JSON.
JSON_PROGRAM_ENVELOPE_RULES = """Output rules:
- Reply with ONLY one JSON object. No markdown code fences, no prose before or after.
- Schema: {{"dialect": "<string>", "program": ["<line>", ...]}}
- Each "program" entry must be one complete source line starting with a line number (e.g. 10 PRINT \\"HELLO\\").
- Line numbers must be UNIQUE in your output. List lines in ascending line-number order (10, 20, 30, ...). Leave gaps for GOSUB targets (e.g. jump to 500 means no other line may use 500).
- The host may auto-renumber duplicate labels and fix GOTO/GOSUB/THEN targets, but you should still avoid duplicates — wrong duplicates can mis-route branches before repair.
- Use double quotes for strings; escape internal quotes as \\"."""

JSON_COMPLETE_PROGRAM_RULE = (
    "- Return the COMPLETE program (every numbered line), not a patch or diff."
)

SHARED_VALIDITY_DIRECTIVES = """
Validity-first rules (strict parser / AIBASIC host):
- Do not copy syntax from QuickBASIC, QB64, GW-BASIC extensions, or Visual BASIC unless it matches the rules below.
- Prefer a smaller correct program over a large one that uses uncertain file or graphics features.
- For persistence, use sequential text files (PRINT#/LINE INPUT#), not random/record I/O.
- SAVE and LOAD are a pair: the number and order of fields written per record must match what each load iteration reads.
""".strip()

COMPACT_SYNTAX_CONTRACT = """
Syntax reminders:
- One physical line in the program = one line number. No duplicate line numbers anywhere (common model mistake: restarting at 200 after already using 200 for the menu).
- ':' separates multiple statements on the same numbered line.
- LET, IF...THEN...ELSE, FOR...NEXT, GOSUB/RETURN.
- OPEN "name" FOR INPUT|OUTPUT|APPEND AS #n only (never FOR RANDOM/BINARY; never OPEN "R",...).
""".strip()

INTERNAL_CHECKLIST_GENERATE = """
Before you answer, mentally verify: every line number is unique, numbers strictly increase down the program list,
GOSUB targets do not collide with other sections (if menu uses 200–220, subroutines must start above 230 or below 190);
names and type suffixes stay consistent; control flow is balanced; output is one JSON object with a complete runnable program.
If the program saves and loads data: count PRINT # lines per record in SAVE and LINE INPUT # (or INPUT #) lines
per record in LOAD — they must match.
""".strip()

INTERNAL_CHECKLIST_FIX = """
Before you answer, mentally verify: any reported failing construct is changed, removed, or replaced;
the full program has no duplicate line numbers; the output must not repeat a known-invalid line unchanged;
variables and suffixes stay consistent; no previously reported invalid syntax remains; validity beats preserving risky syntax.
If the failure is EOF / input past end of file on LINE INPUT#: reconcile SAVE (PRINT# count per record) with LOAD
(LINE INPUT# count per loop iteration).
""".strip()

INTERNAL_CHECKLIST_MERGE = """
Before you answer, mentally verify: you return the full revised program with every line number unique;
unrelated lines stay stable; changes are minimal and additive where possible; you do not refactor into riskier syntax.
If the user describes a bug, wrong behavior, or a runtime error, assume it is real: change the minimal lines
needed to address it (e.g. EOF guards, matching PRINT#/LINE INPUT# record layout). Do not return the same
program unchanged — the host will reject identical output on merge.
If you change menu options or line numbers, re-check every IF CHOICE...THEN GOSUB so each option dispatches
to the right REM/subroutine block (not to a different menu arm left over from old numbering).
""".strip()

RETRY_EXTRA_GENERATE = """
IMPORTANT (retry): The previous output failed validation or parsing. Produce a SMALLER, SIMPLER program.
If duplicate line number: follow the hundreds-block layout in the system prompt (menu 100–189, subs 200+, never reuse a number).
If DIM/CLS/SPLIT: use DIM A(50) only for arrays; scalars as COUNT%=0; no CLS; no SPLIT — LINE INPUT # and string functions only.
If OPEN/FOR/GET/PUT/COMMA: sequential files only (FOR INPUT/OUTPUT/APPEND; LINE INPUT#/PRINT#).
If SAVE/LOAD mismatch or EOF on load: make the same number of file lines per record on write as on read
(e.g. four PRINT # and four LINE INPUT # per entry, or one of each with parsing).
If LINE INPUT#: one variable per statement only — never LINE INPUT #1, A$; B$; use four lines or LINE INPUT #1, R$ then MID$/INSTR.
If PRINT then RETURN on the same line: use a colon before RETURN (e.g. PRINT \"x\": RETURN), not semicolon before RETURN.
Preserve user intent with a dumb-but-valid design rather than repeating the same invalid constructs.
""".strip()

RETRY_EXTRA_FIX = """
IMPORTANT (retry): The previous fix failed validation. The corrected program MUST differ from the input.
The failing line or construct MUST change. Simplify aggressively if needed; validity comes first.
""".strip()

RETRY_EXTRA_MERGE = """
IMPORTANT (retry): The previous merge failed validation or was rejected. Preserve most of the original program;
make only minimal additive changes. Use simpler syntax when uncertain.
If the rejection was IDENTICAL OUTPUT: you must change at least one numbered line versus the current program
(fix the reported bug, add EOF/INPUT# guards, or align file I/O so save/load use the same record shape).
If validation failed on menu GOSUB: each IF CHOICE=n THEN GOSUB x must target the subroutine for option n,
not another IF CHOICE line (renumber subroutines or fix every GOSUB after changing the menu).
""".strip()


def _system_prompt_generate(dialect: str) -> str:
    return (
        "You are a code generator for MBASIC 5.21 / Microsoft BASIC-80 as implemented in "
        "MBASIC-2025.\n\n"
        f"{JSON_PROGRAM_ENVELOPE_RULES}\n"
        f"- {JSON_COMPLETE_PROGRAM_RULE}\n"
        f"{SHARED_VALIDITY_DIRECTIVES}\n\n"
        f"{COMPACT_SYNTAX_CONTRACT}\n\n"
        f"{INTERNAL_CHECKLIST_GENERATE}\n\n"
        f"{MBASIC_AI_LINE_NUMBER_PLAN}\n\n"
        f"{MBASIC_AI_GENERATION_RULES}\n\n"
        "Type suffixes: string $, integer %, single !, double #; keep names and suffixes consistent.\n"
        "Tiny valid examples: 10 PRINT \"HELLO\" / 20 IF X = 1 THEN GOTO 100 / "
        "30 FOR I = 1 TO 10 / 40 NEXT I\n\n"
        f'JSON \"dialect\" field must be exactly: {dialect}\n\n'
        "User request (generate a program):"
    )


def _system_prompt_merge(dialect: str) -> str:
    return (
        "You revise MBASIC 5.21 programs. The user sends the full current program and a "
        "feature or change request (often a bug report or new behavior).\n\n"
        f"{JSON_PROGRAM_ENVELOPE_RULES}\n"
        f"- {JSON_COMPLETE_PROGRAM_RULE}\n"
        f"{SHARED_VALIDITY_DIRECTIVES}\n"
        "- Return the complete revised program, not a patch. Preserve existing structure where practical.\n"
        "- Make only the changes needed; do not upgrade unrelated code into riskier syntax.\n"
        "- Prefer additive edits over large rewrites; keep line numbering style where practical.\n"
        "- If the request implies the program is wrong or misbehaves, your output must differ from the "
        "input: edit the relevant routines. Returning the same source when the user asked for a fix is a "
        "failed response (the host may reject it).\n"
        "- When the user quotes a runtime error (line number, EOF, etc.), trace that path and fix it; "
        "common issues: SAVE writes one line per record but LOAD uses multiple LINE INPUT# per record "
        "(or vice versa) — make them match.\n"
        "- Menu programs: every IF CHOICE=n THEN GOSUB label must jump to the correct subroutine entry "
        "(the REM or first line of that routine). After you add menu lines or renumber, update ALL GOSUB "
        "targets — do not leave GOSUB pointing at a line that is still part of the menu (another "
        "IF CHOICE=... branch).\n\n"
        f"{COMPACT_SYNTAX_CONTRACT}\n\n"
        f"{INTERNAL_CHECKLIST_MERGE}\n\n"
        f"{MBASIC_AI_LINE_NUMBER_PLAN}\n\n"
        f"{MBASIC_AI_GENERATION_RULES}\n\n"
        "Type suffixes: string $, integer %, single !, double #; keep names and suffixes consistent.\n"
        f'JSON \"dialect\" field must be exactly: {dialect}\n'
    )


def _system_prompt_fix(dialect: str) -> str:
    return (
        "You fix MBASIC 5.21 programs after parser failure, runtime failure, or user complaint.\n\n"
        f"{JSON_PROGRAM_ENVELOPE_RULES}\n"
        f"- {JSON_COMPLETE_PROGRAM_RULE}\n"
        f"{SHARED_VALIDITY_DIRECTIVES}\n"
        "- Return a complete corrected program (JSON envelope requires every numbered line). "
        "Make minimal edits: keep lines that are already valid unchanged when possible.\n"
        "- If an error was reported, the output must be meaningfully "
        "different from the input; do not repeat a known-invalid line unchanged.\n"
        "- Preserve user intent where possible; when uncertain, simplify rather than keep risky syntax.\n\n"
        f"{COMPACT_SYNTAX_CONTRACT}\n\n"
        f"{INTERNAL_CHECKLIST_FIX}\n\n"
        f"{MBASIC_AI_LINE_NUMBER_PLAN}\n\n"
        f"{MBASIC_AI_GENERATION_RULES}\n\n"
        "Type suffixes: string $, integer %, single !, double #; keep names and suffixes consistent.\n"
        f'JSON \"dialect\" field must be exactly: {dialect}\n'
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

    def generate(
        self,
        prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        if verbose:
            _verbose_section(
                "fixture generate (request)",
                f"dialect_spec={dialect_spec!r}\nprompt={prompt!r}",
            )
            _verbose_section(
                "fixture generate (response lines)",
                "\n".join(FIXTURE_LINES),
            )
        return GenerationResult(ok=True, lines=list(FIXTURE_LINES))

    def merge_program(
        self,
        existing_source: str,
        user_prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        base = [ln.strip() for ln in existing_source.splitlines() if ln.strip()]
        if not base:
            return GenerationResult(ok=False, lines=[], error="NO PROGRAM IN MEMORY")
        n = _fixture_next_line_num(base)
        snippet = user_prompt.replace("\n", " ")[:60]
        out = base + [f"{n} REM AIMERGE: {snippet}"]
        if verbose:
            _verbose_section(
                "fixture merge (request)",
                f"dialect_spec={dialect_spec!r}\nuser_prompt={user_prompt!r}\n"
                f"--- existing_source ---\n{existing_source}",
            )
            _verbose_section("fixture merge (response lines)", "\n".join(out))
        return GenerationResult(ok=True, lines=out)

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
        *,
        syntax_errors: Optional[str] = None,
        verbose: bool = False,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        base = [ln.strip() for ln in existing_source.splitlines() if ln.strip()]
        if not base:
            return GenerationResult(ok=False, lines=[], error="NO PROGRAM IN MEMORY")
        n = _fixture_next_line_num(base)
        out = base + [f"{n} REM AIFIX"]
        if verbose:
            _verbose_section(
                "fixture fix (request)",
                f"dialect_spec={dialect_spec!r}\n"
                f"error_context={error_context!r}\nuser_hint={user_hint!r}\n"
                f"syntax_errors={syntax_errors!r}\n"
                f"--- existing_source ---\n{existing_source}",
            )
            _verbose_section("fixture fix (response lines)", "\n".join(out))
        return GenerationResult(ok=True, lines=out)

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
        verbose: bool = False,
    ) -> ExplainResult:
        if line_number is not None:
            text = f"FIXTURE: Line {line_number} (program {len(existing_source)} chars)."
        else:
            text = "FIXTURE: Whole program summary (fixture backend)."
        if verbose:
            _verbose_section(
                "fixture explain (request)",
                f"dialect_spec={dialect_spec!r}\nline_number={line_number!r}\n"
                f"--- existing_source ---\n{existing_source}",
            )
            _verbose_section("fixture explain (response text)", text)
        return ExplainResult(ok=True, text=text)


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

    def _post_chat(
        self, system: str, user: str, *, verbose: bool = False
    ) -> Tuple[bool, str, Optional[str]]:
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        if verbose:
            _verbose_section(
                "remote chat request (JSON body; API key is only in HTTP headers)",
                json.dumps(body, indent=2, ensure_ascii=False),
            )
            _verbose_section("remote chat endpoint", self.base_url)
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
            if verbose:
                _verbose_section(
                    "remote chat HTTP error body (truncated)",
                    detail or e.reason,
                )
            return False, "", f"AI HTTP {e.code}: {detail or e.reason}"
        except urllib.error.URLError as e:
            if verbose:
                _verbose_section("remote chat URL error", str(e.reason))
            return False, "", f"AI network error: {e.reason}"
        except TimeoutError:
            if verbose:
                _verbose_section("remote chat", "request timed out")
            return False, "", "AI request timed out"

        if verbose:
            _verbose_section("remote chat HTTP response body", raw)

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
        if verbose:
            _verbose_section("remote chat assistant message (extracted)", content)
        return True, content, None

    def _generate_with_validation_retry(
        self,
        *,
        dialect_spec: str,
        def_type_map: Optional[dict],
        verbose: bool,
        operation: str,
        system_base: str,
        retry_extra: str,
        user: str,
        fix_input_source: Optional[str] = None,
        syntax_errors: Optional[str] = None,
        merge_base_source: Optional[str] = None,
    ) -> GenerationResult:
        """Up to two model calls: first normal prompt, then one conservative retry on validation failure."""
        last_err: Optional[str] = None
        last_extracted: Optional[list[str]] = None
        for attempt in range(2):
            user_msg = user
            if attempt == 1:
                print("RETRYING AI REQUEST (CONSERVATIVE)")
                retry_body = retry_extra
                if last_err:
                    retry_body += (
                        "\n\nThe host rejected your previous program (summary below). "
                        "The user message lists EVERY issue with BASIC line numbers where known — "
                        "fix all of them, not only the first.\n\n"
                        f"First failing check (summary): {last_err}"
                    )
                system = f"{system_base}\n\n{retry_body}"
                if last_extracted:
                    diag_ctx = ProgramValidationContext(
                        dialect_spec=dialect_spec,
                        def_type_map=def_type_map,
                        operation=operation,
                        fix_input_source=fix_input_source,
                        syntax_errors=syntax_errors,
                    )
                    diag_block = format_host_diagnostics_for_retry(
                        list(last_extracted), diag_ctx
                    )
                    parts = [user, "---"]
                    if diag_block.strip():
                        parts.append(
                            "Host diagnostics — fix EVERY numbered item (BASIC line numbers refer to "
                            "the failing program after host renumber, LINE INPUT expansion, and "
                            "'; RETURN' -> ': RETURN' repair):\n"
                            + diag_block
                        )
                        parts.append("---")
                    parts.append(
                        "Your previous model output (failed validation/parse). "
                        "Return a corrected full program; change every invalid line; "
                        "do not repeat the same mistakes:\n"
                        + "\n".join(last_extracted)
                    )
                    user_msg = "\n\n".join(parts)
            else:
                system = system_base
            ok, content, err = self._post_chat(system, user_msg, verbose=verbose)
            if not ok:
                return GenerationResult(
                    ok=False,
                    lines=list(last_extracted) if last_extracted else [],
                    error=err or "AI REQUEST FAILED",
                )
            ext_ok, lines, perr = extract_program_from_content(content, dialect_spec)
            if not ext_ok:
                last_err = perr or "AI OUTPUT FAILED VALIDATION"
                continue
            last_extracted = lines
            ctx = ProgramValidationContext(
                dialect_spec=dialect_spec,
                def_type_map=def_type_map,
                operation=operation,
                fix_input_source=fix_input_source,
                syntax_errors=syntax_errors,
            )
            verr = validate_ai_program(lines, ctx)
            if verr is None:
                if (
                    operation == "merge"
                    and merge_base_source is not None
                    and merge_output_is_identical_to_base(merge_base_source, lines)
                ):
                    last_err = _MERGE_IDENTICAL_ERR
                    last_extracted = list(lines)
                    continue
                return GenerationResult(ok=True, lines=lines)
            last_err = verr
        if (
            operation == "merge"
            and merge_base_source is not None
            and last_extracted is not None
            and merge_output_is_identical_to_base(merge_base_source, last_extracted)
        ):
            return GenerationResult(
                ok=False,
                lines=list(last_extracted),
                error=last_err or _MERGE_IDENTICAL_ERR,
            )
        return GenerationResult(
            ok=False,
            lines=list(last_extracted) if last_extracted else [],
            error=last_err or "AI OUTPUT FAILED",
        )

    def generate(
        self,
        prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        return self._generate_with_validation_retry(
            dialect_spec=dialect_spec,
            def_type_map=def_type_map,
            verbose=verbose,
            operation="generate",
            system_base=_system_prompt_generate(dialect_spec),
            retry_extra=RETRY_EXTRA_GENERATE,
            user=prompt,
        )

    def merge_program(
        self,
        existing_source: str,
        user_prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        user = (
            f"Current program:\n{existing_source}\n\n"
            f"Modification request:\n{user_prompt}\n"
        )
        return self._generate_with_validation_retry(
            dialect_spec=dialect_spec,
            def_type_map=def_type_map,
            verbose=verbose,
            operation="merge",
            system_base=_system_prompt_merge(dialect_spec),
            retry_extra=RETRY_EXTRA_MERGE,
            user=user,
            merge_base_source=existing_source.strip(),
        )

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
        *,
        syntax_errors: Optional[str] = None,
        verbose: bool = False,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        syn_part = syntax_errors or "(none)"
        err_part = error_context or "(none)"
        hint_part = user_hint or "(none)"
        user = (
            f"Current program:\n{existing_source}\n\n"
            f"Syntax / parser messages:\n{syn_part}\n\n"
            f"Runtime error context:\n{err_part}\n\n"
            f"User hint:\n{hint_part}\n"
        )
        return self._generate_with_validation_retry(
            dialect_spec=dialect_spec,
            def_type_map=def_type_map,
            verbose=verbose,
            operation="fix",
            system_base=_system_prompt_fix(dialect_spec),
            retry_extra=RETRY_EXTRA_FIX,
            user=user,
            fix_input_source=existing_source,
            syntax_errors=syntax_errors,
        )

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
        verbose: bool = False,
    ) -> ExplainResult:
        if line_number is not None:
            user = (
                f"Dialect: {dialect_spec}\n"
                f"Focus on line number: {line_number}\n\n"
                f"Program:\n{existing_source}\n"
            )
        else:
            user = f"Dialect: {dialect_spec}\n\nProgram:\n{existing_source}\n"
        ok, content, err = self._post_chat(EXPLAIN_SYSTEM, user, verbose=verbose)
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

    def generate(
        self,
        prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        if verbose:
            _verbose_section("error backend (no request sent)", self._message)
        return GenerationResult(ok=False, lines=[], error=self._message)

    def merge_program(
        self,
        existing_source: str,
        user_prompt: str,
        dialect_spec: str,
        verbose: bool = False,
        *,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        if verbose:
            _verbose_section("error backend (no request sent)", self._message)
        return GenerationResult(ok=False, lines=[], error=self._message)

    def fix_program(
        self,
        existing_source: str,
        error_context: Optional[str],
        user_hint: Optional[str],
        dialect_spec: str,
        *,
        syntax_errors: Optional[str] = None,
        verbose: bool = False,
        def_type_map: Optional[dict] = None,
    ) -> GenerationResult:
        if verbose:
            _verbose_section("error backend (no request sent)", self._message)
        return GenerationResult(ok=False, lines=[], error=self._message)

    def explain_program(
        self,
        existing_source: str,
        line_number: Optional[int],
        dialect_spec: str,
        verbose: bool = False,
    ) -> ExplainResult:
        if verbose:
            _verbose_section("error backend (no request sent)", self._message)
        return ExplainResult(ok=False, text="", error=self._message)
