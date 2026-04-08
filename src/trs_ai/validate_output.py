"""Host-side validation for AI-generated MBASIC programs (recipe: schema, lines, parse, light lints)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from src.trs_ai.parse_response import strip_markdown_fences

_LINE_START = re.compile(r"^(\d+)\s")
# Match DEF USR, DEF USR0, etc. (not implemented in this runtime).
_FORBIDDEN_DEF_USR = re.compile(r"\bDEF\s+USR\d*", re.IGNORECASE)
# Parser: OPEN "file" FOR ... only allows INPUT, OUTPUT, APPEND — not RANDOM/BINARY.
_FOR_OPEN_FOR_RANDOM = re.compile(
    r"\bOPEN\b[^:\n]*\bFOR\s+(RANDOM|BINARY)\b", re.IGNORECASE
)
# Classic random mode OPEN "R", ... — rejected for AIBASIC (use sequential I/O only).
_FOR_OPEN_QUOTE_R = re.compile(r'\bOPEN\s*"(?:R|r)"\s*,', re.IGNORECASE)
# GET #n, rec, var — only GET #n [, rec] is valid; a second comma means MS-style junk.
_GET_PUT_EXTRA_COMMA = re.compile(
    r"\b(GET|PUT)\s+#[^:\n]*,\s*[^:\n]*,", re.IGNORECASE
)
# FIELD / record-buffer style I/O — not generated for this appliance dialect.
_FORBIDDEN_FIELD = re.compile(r"\bFIELD\s+#", re.IGNORECASE)
# Trailing \b fails for e.g. A!=2 (! followed by =). Disallow suffix followed by alnum.
_SUFFIXED_ID = re.compile(r"\b([A-Za-z][A-Za-z0-9]*)([%$#!])(?![A-Za-z0-9])")
_ERROR_LINE_NUM = re.compile(r"(?:Parse error at line |at line )(\d+)")
_FORBIDDEN_CLS = re.compile(r"\bCLS\b", re.IGNORECASE)
_FORBIDDEN_SPLIT = re.compile(r"\bSPLIT\s+", re.IGNORECASE)
# LINE INPUT #f, var — only one string var; models hallucinate N$; E$; D$
_LINE_INPUT_MULTI_SEMI = re.compile(
    r"\bLINE INPUT\s+#[^,\n]+,\s*[^;\n]+;",
    re.IGNORECASE,
)
# One LINE INPUT file statement (leading); group 1 = "LINE INPUT #n", group 2 = "v1; v2; ..."
_LINE_INPUT_FILE_STMT = re.compile(
    r"^\s*(LINE\s+INPUT\s+#\s*\d+)\s*,\s*(.+)$",
    re.IGNORECASE | re.DOTALL,
)
# Menu dispatch: IF CHOICE=n THEN GOSUB label — target must not be another menu arm.
_MENU_IF_THEN_GOSUB = re.compile(
    r"IF\s+CHOICE\s*=\s*\d+\s+THEN\s+GOSUB\s+(\d+)",
    re.IGNORECASE,
)
_MENU_IF_BRANCH_START = re.compile(
    r"^\s*IF\s+CHOICE\s*=\s*\d+\s+THEN\b",
    re.IGNORECASE,
)
_LEADING_LINE_NUM = re.compile(r"^(\d+)\s+(.*)$", re.DOTALL)


@dataclass
class ProgramValidationContext:
    """Context for validating an extracted AI program."""

    dialect_spec: str
    def_type_map: Optional[dict]
    operation: str  # "generate" | "fix" | "merge"
    fix_input_source: Optional[str] = None
    syntax_errors: Optional[str] = None


def extract_program_from_content(
    content: str, dialect_spec: str
) -> Tuple[bool, List[str], Optional[str]]:
    """
    Parse assistant content into program lines.
    JSON objects must carry dialect matching dialect_spec; plain numbered lines are accepted as fallback.
    """
    raw = strip_markdown_fences(content)
    if not raw:
        return False, [], "AI OUTPUT FAILED VALIDATION: empty response"

    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            got = data.get("dialect")
            if not isinstance(got, str) or got.strip() != dialect_spec:
                return False, [], "AI OUTPUT FAILED VALIDATION: dialect mismatch"
            prog = data.get("program")
            if prog is None:
                return False, [], 'AI OUTPUT FAILED VALIDATION: missing "program"'
            if not isinstance(prog, list):
                return False, [], 'AI OUTPUT FAILED VALIDATION: "program" must be an array'
            out: List[str] = []
            for i, item in enumerate(prog):
                if not isinstance(item, str):
                    return (
                        False,
                        [],
                        f'AI OUTPUT FAILED VALIDATION: program[{i}] must be a string',
                    )
                line = item.strip()
                if not line:
                    continue
                if not _LINE_START.match(line):
                    return (
                        False,
                        [],
                        "AI OUTPUT FAILED VALIDATION: program line must start with a line number",
                    )
                out.append(line)
            if not out:
                return False, [], "AI OUTPUT FAILED VALIDATION: program is empty"
            return True, out, None
    except json.JSONDecodeError:
        pass

    lines: List[str] = []
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        if _LINE_START.match(s):
            lines.append(s)
    if lines:
        return True, lines, None
    return False, [], "AI OUTPUT FAILED VALIDATION: no valid JSON program or numbered lines"


def _duplicate_line_check(lines: List[str]) -> Optional[str]:
    seen: set[int] = set()
    for raw in lines:
        m = _LINE_START.match(raw.strip())
        if not m:
            return "AI OUTPUT FAILED VALIDATION: line without leading line number"
        n = int(m.group(1))
        if n in seen:
            return (
                f"AI OUTPUT FAILED VALIDATION: duplicate line number {n} "
                "(each BASIC line number must appear exactly once; renumber the whole program)"
            )
        seen.add(n)
    return None


def _has_duplicate_line_numbers(lines: List[str]) -> bool:
    seen: set[int] = set()
    for raw in lines:
        m = _LINE_START.match(raw.strip())
        if not m:
            continue
        n = int(m.group(1))
        if n in seen:
            return True
        seen.add(n)
    return False


_LBL_PH = "«LBL{0}»"  # must not appear in BASIC source


def _replace_line_targets_in_unquoted(text: str, ref_map: Dict[int, int]) -> str:
    """
    Rewrite GOTO/GOSUB/THEN numeric targets using ref_map (old label -> new label).

    Placeholder pass avoids double-mapping: THEN GOSUB 200 -> THEN GOSUB 270 must not
    then treat 270 as old line 270 (would jump to the wrong routine).
    """
    old_labels = set(ref_map.keys())

    def mark_then_gosub(m) -> str:
        n = int(m.group(1))
        if n not in old_labels:
            return m.group(0)
        return f"THEN GOSUB {_LBL_PH.format(n)}"

    def mark_gosub(m) -> str:
        n = int(m.group(1))
        if n not in old_labels:
            return m.group(0)
        return f"GOSUB {_LBL_PH.format(n)}"

    def mark_goto(m) -> str:
        n = int(m.group(1))
        if n not in old_labels:
            return m.group(0)
        return f"GOTO {_LBL_PH.format(n)}"

    def mark_then_line(m) -> str:
        n = int(m.group(1))
        if n not in old_labels:
            return m.group(0)
        return f"THEN {_LBL_PH.format(n)}"

    text = re.sub(
        r"\bTHEN\s+GOSUB\s+(\d+)\b",
        mark_then_gosub,
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\bGOSUB\s+(\d+)\b", mark_gosub, text, flags=re.IGNORECASE)
    text = re.sub(r"\bGOTO\s+(\d+)\b", mark_goto, text, flags=re.IGNORECASE)
    text = re.sub(r"\bTHEN\s+(\d+)\b", mark_then_line, text, flags=re.IGNORECASE)

    for old in old_labels:
        text = text.replace(_LBL_PH.format(old), str(ref_map[old]))
    return text


def _replace_line_number_refs_in_body(body: str, ref_map) -> str:
    """Apply target replacement only outside double-quoted strings."""
    parts = body.split('"')
    out: List[str] = []
    for i, seg in enumerate(parts):
        if i % 2 == 0:
            out.append(_replace_line_targets_in_unquoted(seg, ref_map))
        else:
            out.append(seg)
    return '"'.join(out)


def renumber_duplicate_line_numbers(lines: List[str]) -> List[str]:
    """
    If duplicate BASIC line numbers exist, assign fresh unique numbers in source order
    (100, 110, 120, ...) and rewrite GOTO/GOSUB/THEN targets.

    For a duplicated label N, the **last** source line that used N becomes the target of
    GOTO/GOSUB/THEN N (common LLM pattern: menu uses 200, then 200 REM subroutine).
    """
    if not _has_duplicate_line_numbers(lines):
        return list(lines)

    parsed: List[Tuple[int, str]] = []
    for raw in lines:
        m = _LEADING_LINE_NUM.match(raw.strip())
        if not m:
            continue
        parsed.append((int(m.group(1)), m.group(2).rstrip()))

    n = len(parsed)
    new_nums = [100 + 10 * i for i in range(n)]

    old_to_last_idx: Dict[int, int] = {}
    for i, (old, _) in enumerate(parsed):
        old_to_last_idx[old] = i

    ref_map = {old: new_nums[j] for old, j in old_to_last_idx.items()}

    out: List[str] = []
    for i, (old, body) in enumerate(parsed):
        new_body = _replace_line_number_refs_in_body(body, ref_map)
        out.append(f"{new_nums[i]} {new_body}")
    return out


def apply_line_number_repair_if_needed(lines: List[str]) -> None:
    """Mutate lines in place when duplicates are detected (host-side appliance repair)."""
    if not lines or not _has_duplicate_line_numbers(lines):
        return
    fixed = renumber_duplicate_line_numbers(lines)
    lines.clear()
    lines.extend(fixed)


def _repair_one_statement_line_input_multi_var(stmt: str) -> str:
    """
    LINE INPUT #f, A$; B$; C$ -> LINE INPUT #f, A$: LINE INPUT #f, B$: ...
    Leaves non-LINE-INPUT statements unchanged.
    """
    stripped = stmt.strip()
    m = _LINE_INPUT_FILE_STMT.match(stripped)
    if not m:
        return stmt
    rest = m.group(2).strip()
    if ";" not in rest:
        return stmt
    vars_list = [v.strip() for v in rest.split(";") if v.strip()]
    if len(vars_list) < 2:
        return stmt
    ch_m = re.search(r"#\s*\d+", m.group(1), re.I)
    if not ch_m:
        return stmt
    ch = re.sub(r"\s+", "", ch_m.group(0))
    pieces = [f"LINE INPUT {ch}, {vars_list[0]}"]
    for v in vars_list[1:]:
        pieces.append(f"LINE INPUT {ch}, {v}")
    new_inner = ": ".join(pieces)
    lead = stmt[: len(stmt) - len(stmt.lstrip())]
    return lead + new_inner


def _repair_body_line_input_multi_var(body: str) -> str:
    if not _LINE_INPUT_MULTI_SEMI.search(body):
        return body
    if ":" not in body:
        return _repair_one_statement_line_input_multi_var(body)
    parts = body.split(":")
    return ":".join(_repair_one_statement_line_input_multi_var(p) for p in parts)


def apply_line_input_multi_var_repair_if_needed(lines: List[str]) -> None:
    """Mutate lines: expand invalid LINE INPUT #f, A$; B$ into chained single-var reads."""
    for i, raw in enumerate(lines):
        m = _LEADING_LINE_NUM.match(raw.strip())
        if not m:
            continue
        num, body = m.group(1), m.group(2)
        new_body = _repair_body_line_input_multi_var(body)
        if new_body != body:
            lines[i] = f"{num} {new_body}"


def _repair_semicolon_before_return_outside_strings(body: str) -> str:
    """
    Models often emit PRINT \"...\"; RETURN or THEN ...; RETURN — ';' continues PRINT list,
    so RETURN is a parse error. Use ':' as the statement separator before RETURN.
    """
    parts = body.split('"')
    out: List[str] = []
    for i, seg in enumerate(parts):
        if i % 2 == 0:
            out.append(re.sub(r";\s*RETURN\b", ": RETURN", seg, flags=re.IGNORECASE))
        else:
            out.append(seg)
    return '"'.join(out)


def apply_semicolon_return_repair_if_needed(lines: List[str]) -> None:
    """Mutate lines: '; RETURN' -> ': RETURN' outside string literals."""
    for i, raw in enumerate(lines):
        m = _LEADING_LINE_NUM.match(raw.strip())
        if not m:
            continue
        num, body = m.group(1), m.group(2)
        new_body = _repair_semicolon_before_return_outside_strings(body)
        if new_body != body:
            lines[i] = f"{num} {new_body}"


def _line_dict(lines: List[str]) -> Dict[int, str]:
    d: Dict[int, str] = {}
    for raw in lines:
        m = _LINE_START.match(raw.strip())
        if m:
            d[int(m.group(1))] = raw.strip()
    return d


def _normalize_program_text(text: str) -> str:
    return "\n".join(s.strip() for s in text.strip().splitlines() if s.strip())


def _dim_first_declarator_missing_open_paren(after_dim: str) -> bool:
    """True if first DIM declarator has no '(' (parser requires DIM only for arrays)."""
    after_dim = after_dim.strip()
    depth = 0
    i = 0
    while i < len(after_dim):
        c = after_dim[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "," and depth == 0:
            break
        i += 1
    first = after_dim[:i].strip()
    return "(" not in first


def lint_dim_invalid(lines: List[str]) -> Optional[str]:
    """
    MBASIC parser requires DIM x(dims); scalars like DIM COUNT% are a parse error.
    """
    for raw in lines:
        body = _LINE_START.sub("", raw.strip(), count=1).strip()
        if not body:
            continue
        for part in body.split(":"):
            p = part.strip()
            if '"' in p:
                continue
            if not re.match(r"DIM\s+", p, re.I):
                continue
            after = re.split(r"DIM\s+", p, maxsplit=1, flags=re.I)[1].strip()
            if _dim_first_declarator_missing_open_paren(after):
                return (
                    "AI OUTPUT FAILED VALIDATION: DIM may only declare arrays with "
                    "parentheses, e.g. DIM N$(50); use COUNT%=0 not DIM COUNT%"
                )
    return None


def lint_menu_gosub_targets(lines: List[str]) -> Optional[str]:
    """
    LLM merges often extend the menu but leave stale GOSUB lines (jump into another IF CHOICE arm).
    Example: IF CHOICE=1 THEN GOSUB 280 while line 280 is IF CHOICE=7 THEN END.
    """
    line_by_num: Dict[int, str] = {}
    for raw in lines:
        m = _LINE_START.match(raw.strip())
        if m:
            line_by_num[int(m.group(1))] = raw.strip()

    for raw in lines:
        s = raw.strip()
        m = _LINE_START.match(s)
        if not m:
            continue
        body = _LINE_START.sub("", s, count=1).strip()
        for gosub_m in _MENU_IF_THEN_GOSUB.finditer(body):
            tgt = int(gosub_m.group(1))
            tline = line_by_num.get(tgt)
            if tline is None:
                continue
            tbody = _LINE_START.sub("", tline.strip(), count=1).strip()
            for part in tbody.split(":"):
                p = part.strip()
                if not p:
                    continue
                if _MENU_IF_BRANCH_START.match(p):
                    return (
                        "AI OUTPUT FAILED VALIDATION: menu IF CHOICE...THEN GOSUB points to line "
                        f"{tgt}, which is another IF CHOICE branch (stale target after menu edit). "
                        "Point each GOSUB at the correct subroutine (REM) line."
                    )
    return None


def lint_forbidden_syntax(lines: List[str]) -> Optional[str]:
    blob = "\n".join(lines)
    if _FORBIDDEN_CLS.search(blob):
        return (
            "AI OUTPUT FAILED VALIDATION: CLS is not implemented in this interpreter "
            "(omit it or use PRINT \"\" for spacing)"
        )
    if _FORBIDDEN_SPLIT.search(blob):
        return (
            "AI OUTPUT FAILED VALIDATION: SPLIT is not a statement (parse fields with "
            "MID$/INSTR or one LINE INPUT per field)"
        )
    if _LINE_INPUT_MULTI_SEMI.search(blob):
        return (
            "AI OUTPUT FAILED VALIDATION: LINE INPUT #f, var allows only one variable "
            "(use four LINE INPUT # lines or one LINE INPUT whole line and parse with MID$)"
        )
    err = lint_dim_invalid(lines)
    if err:
        return err
    if _FORBIDDEN_DEF_USR.search(blob):
        return "AI OUTPUT FAILED VALIDATION: unsupported syntax (DEF USR)"
    if _FOR_OPEN_FOR_RANDOM.search(blob):
        return (
            "AI OUTPUT FAILED VALIDATION: OPEN ... FOR RANDOM/BINARY is invalid here "
            "(only FOR INPUT, OUTPUT, or APPEND); use sequential PRINT#/INPUT#/LINE INPUT#"
        )
    if _FOR_OPEN_QUOTE_R.search(blob):
        return (
            'AI OUTPUT FAILED VALIDATION: OPEN "R" random mode not allowed in AI programs '
            "(use sequential file lines only)"
        )
    if _GET_PUT_EXTRA_COMMA.search(blob):
        return (
            "AI OUTPUT FAILED VALIDATION: GET/PUT must not use MS-style "
            "GET #f, rec, var$ / PUT #f, rec, var$ (use LINE INPUT#/PRINT# per line)"
        )
    if _FORBIDDEN_FIELD.search(blob):
        return (
            "AI OUTPUT FAILED VALIDATION: FIELD / random-record buffer I/O "
            "not allowed in AI programs"
        )
    err = lint_menu_gosub_targets(lines)
    if err:
        return err
    return None


def lint_suffix_consistency(lines: List[str]) -> Optional[str]:
    """Flag the same identifier base with two different explicit type suffixes."""
    text = "\n".join(lines)
    by_base: Dict[str, set] = {}
    for m in _SUFFIXED_ID.finditer(text):
        b = m.group(1).upper()
        by_base.setdefault(b, set()).add(m.group(2))
    for sufs in by_base.values():
        if len(sufs) > 1:
            return "AI OUTPUT FAILED VALIDATION: inconsistent type suffix"
    return None


def first_reported_error_line_number(syntax_errors: Optional[str]) -> Optional[int]:
    if not syntax_errors:
        return None
    m = _ERROR_LINE_NUM.search(syntax_errors)
    return int(m.group(1)) if m else None


def line_text_for_number(source: str, line_num: int) -> Optional[str]:
    for line in source.splitlines():
        s = line.strip()
        m = _LINE_START.match(s)
        if m and int(m.group(1)) == line_num:
            return s
    return None


def lint_identical_fix(output_lines: List[str], fix_input_source: str) -> Optional[str]:
    out = _normalize_program_text("\n".join(output_lines))
    inp = _normalize_program_text(fix_input_source)
    if out == inp:
        return "AI FIX RETURNED NO CHANGES"
    return None


def lint_failing_line_unchanged(
    output_lines: List[str],
    fix_input_source: str,
    syntax_errors: Optional[str],
) -> Optional[str]:
    ln = first_reported_error_line_number(syntax_errors)
    if ln is None:
        return None
    before = line_text_for_number(fix_input_source, ln)
    after = line_text_for_number("\n".join(output_lines), ln)
    if before is None or after is None:
        return None
    if before.strip() == after.strip():
        return "AI FIX DID NOT CHANGE FAILING LINE"
    return None


def validate_parse_all_lines(def_type_map: dict, lines: List[str]) -> Optional[str]:
    """Return an error string if any line fails MBASIC parse."""
    from src.editing import ProgramManager

    tmp = ProgramManager(def_type_map)
    for raw in lines:
        line = raw.strip()
        m = _LINE_START.match(line)
        if not m:
            return "AI OUTPUT FAILED PARSE: line without line number"
        line_num = int(m.group(1))
        ok, err = tmp.add_line(line_num, line)
        if not ok:
            msg = str(err or f"Parse error at line {line_num}")
            if msg.startswith("?"):
                msg = msg[1:].strip()
            return f"AI OUTPUT FAILED PARSE: {msg}"
    return None


def collect_parse_errors_all_lines(def_type_map: dict, lines: List[str]) -> List[str]:
    """
    Every line parsed in isolation — lists all syntax errors with BASIC line numbers.
    Used for LLM retry diagnostics (validate_parse_all_lines stops at the first error).
    """
    from src.editing import ProgramManager

    errors: List[str] = []
    for raw in lines:
        line = raw.strip()
        m = _LINE_START.match(line)
        if not m:
            errors.append("A program line is missing a leading line number")
            continue
        line_num = int(m.group(1))
        tmp = ProgramManager(def_type_map)
        ok, err = tmp.add_line(line_num, line)
        if not ok:
            msg = str(err or f"Parse error at line {line_num}")
            if msg.startswith("?"):
                msg = msg[1:].strip()
            errors.append(f"Line {line_num}: {msg}")
    return errors


def prepare_ai_program_lines_copy(lines: List[str]) -> List[str]:
    """Copy and apply the same host repairs as validate_ai_program (non-mutating on input)."""
    work = list(lines)
    apply_line_number_repair_if_needed(work)
    apply_line_input_multi_var_repair_if_needed(work)
    apply_semicolon_return_repair_if_needed(work)
    return work


def collect_host_diagnostics_for_retry(
    lines: List[str], ctx: ProgramValidationContext
) -> List[str]:
    """
    All host-detected issues with line numbers where applicable, for AI retry user messages.
    Runs the same repairs as validation, then duplicate/lint checks and per-line parse errors.
    """
    work = prepare_ai_program_lines_copy(lines)
    out: List[str] = []
    e = _duplicate_line_check(work)
    if e:
        out.append(e)
    e = lint_forbidden_syntax(work)
    if e:
        out.append(e)
    e = lint_suffix_consistency(work)
    if e:
        out.append(e)
    if ctx.operation == "fix" and ctx.fix_input_source is not None:
        e = lint_identical_fix(work, ctx.fix_input_source)
        if e:
            out.append(e)
        e = lint_failing_line_unchanged(
            work, ctx.fix_input_source, ctx.syntax_errors
        )
        if e:
            out.append(e)
    if ctx.def_type_map is not None:
        out.extend(collect_parse_errors_all_lines(ctx.def_type_map, work))
    return out


def format_host_diagnostics_for_retry(
    lines: List[str], ctx: ProgramValidationContext
) -> str:
    items = collect_host_diagnostics_for_retry(lines, ctx)
    if not items:
        return ""
    return "\n".join(f"{i + 1}. {msg}" for i, msg in enumerate(items))


def validate_ai_program(lines: List[str], ctx: ProgramValidationContext) -> Optional[str]:
    """
    Full pipeline after JSON/plain extraction: structure, lints, parse.
    Returns None if OK, else a terse machine-style error string.
    """
    if not lines:
        return "AI OUTPUT FAILED VALIDATION: empty program"

    apply_line_number_repair_if_needed(lines)
    apply_line_input_multi_var_repair_if_needed(lines)
    apply_semicolon_return_repair_if_needed(lines)

    err = _duplicate_line_check(lines)
    if err:
        return err

    err = lint_forbidden_syntax(lines)
    if err:
        return err

    err = lint_suffix_consistency(lines)
    if err:
        return err

    if ctx.operation == "fix" and ctx.fix_input_source is not None:
        err = lint_identical_fix(lines, ctx.fix_input_source)
        if err:
            return err
        err = lint_failing_line_unchanged(
            lines, ctx.fix_input_source, ctx.syntax_errors
        )
        if err:
            return err

    if ctx.def_type_map is None:
        return None
    return validate_parse_all_lines(ctx.def_type_map, lines)
