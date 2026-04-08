"""Host-side AI program validation (schema, structure, parse, fix lints)."""

from __future__ import annotations

import json
import re

from src.ast_nodes import TypeInfo
from src.trs_ai.backends import merge_output_is_identical_to_base
from src.trs_ai.validate_output import (
    ProgramValidationContext,
    collect_parse_errors_all_lines,
    extract_program_from_content,
    format_host_diagnostics_for_retry,
    lint_failing_line_unchanged,
    lint_identical_fix,
    lint_suffix_consistency,
    renumber_duplicate_line_numbers,
    validate_ai_program,
    _has_duplicate_line_numbers,
)


def _default_def_map():
    return {c: TypeInfo.SINGLE for c in "abcdefghijklmnopqrstuvwxyz"}


def test_menu_gosub_into_another_if_choice_rejected():
    """Merge often leaves GOSUB pointing at old menu line instead of subroutine (not host renumber)."""
    lines = [
        '220 IF CHOICE=1 THEN GOSUB 280',
        "280 IF CHOICE=7 THEN END",
        "300 REM Add Entry Subroutine",
        "310 RETURN",
    ]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "merge")
    err = validate_ai_program(lines, ctx)
    assert err and "GOSUB" in err and "IF CHOICE" in err


def test_menu_gosub_to_rem_passes_lint():
    lines = [
        '200 IF CHOICE=1 THEN GOSUB 300',
        "300 REM Add Entry",
        "310 RETURN",
        "999 END",
    ]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err is None


def test_merge_output_is_identical_to_base_sorts_by_line_number():
    base = "20 END\n10 PRINT \"X\"\n"
    lines = ['10 PRINT "X"', "20 END"]
    assert merge_output_is_identical_to_base(base, lines)
    assert not merge_output_is_identical_to_base(base, ['10 PRINT "Y"', "20 END"])


def test_extract_json_requires_dialect_match():
    payload = {"dialect": "WRONG", "program": ['10 PRINT "X"', "20 END"]}
    ok, lines, err = extract_program_from_content(json.dumps(payload), "AIBASIC-0.1")
    assert not ok
    assert err and "dialect" in err.lower()


def test_extract_json_rejects_line_without_number():
    payload = {"dialect": "AIBASIC-0.1", "program": ['PRINT "BAD"', "20 END"]}
    ok, lines, err = extract_program_from_content(json.dumps(payload), "AIBASIC-0.1")
    assert not ok
    assert "line number" in (err or "").lower()


def test_duplicate_line_numbers_host_repair():
    """Duplicates are renumbered in validate_ai_program so the appliance can accept LLM output."""
    lines = ['10 PRINT "A"', '10 PRINT "B"', "30 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    assert _has_duplicate_line_numbers(lines)
    err = validate_ai_program(lines, ctx)
    assert err is None
    assert not _has_duplicate_line_numbers(lines)
    assert lines[0].startswith("100 ")
    assert lines[1].startswith("110 ")


def test_renumber_gosub_targets_last_duplicate_label():
    out = renumber_duplicate_line_numbers(
        [
            "100 GOSUB 200",
            "150 END",
            "200 PRINT 1",
            "200 PRINT 2",
        ]
    )
    assert out[0].startswith("100 GOSUB ")
    assert "GOSUB 130" in out[0]
    assert out[-1].startswith("130 ")


def test_renumber_no_double_map_when_new_collides_with_old_label():
    """
    GOSUB 200 -> new address N must not be replaced again because some other line
    was originally numbered N (e.g. old 270 INPUT -> new 310 would steal GOSUB 270).
    """
    out = renumber_duplicate_line_numbers(
        [
            "10 GOSUB 200",
            "20 REM",
            "200 IF X=1 THEN GOSUB 500",
            "200 REM SUBSTART",
            "210 PRINT 0",
            "270 INPUT MOBILE",
        ]
    )
    first = out[0]
    g = int(re.search(r"GOSUB\s+(\d+)", first).group(1))
    sub_line = [L for L in out if "SUBSTART" in L][0]
    sub_num = int(sub_line.split()[0])
    mobile_line = [L for L in out if "MOBILE" in L][0]
    mobile_num = int(mobile_line.split()[0])
    assert g == sub_num
    assert g != mobile_num


def test_semicolon_return_host_repaired():
    """LLMs often use PRINT \"...\"; RETURN — parser needs ': RETURN' as next statement."""
    lines = ['10 IF X=1 THEN PRINT "Hi"; RETURN', "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err is None
    assert ": RETURN" in lines[0]
    assert "; RETURN" not in lines[0]


def test_collect_parse_errors_lists_each_bad_line():
    """Diagnostics must not stop at the first parse error (retry user message)."""
    lines = ['10 PRINT "a"; RETURN', '20 PRINT "b"; RETURN', "30 END"]
    errs = collect_parse_errors_all_lines(_default_def_map(), lines)
    assert len(errs) >= 2
    assert all("Line " in e for e in errs)


def test_format_host_diagnostics_includes_multiple_issues():
    """Lint plus per-line parse errors should both appear (not first-error-only)."""
    lines = ['10 PRINT "ok"', "20 CLS", "30 FOO BAR", "40 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    text = format_host_diagnostics_for_retry(lines, ctx)
    assert "CLS" in text
    assert "Line 30:" in text


def test_line_input_multi_variable_host_repaired():
    """Models emit LINE INPUT #f, A$; B$; host expands to one var per statement."""
    lines = ["10 LINE INPUT #1, N$; E$; M$", "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err is None
    assert lines[0].count("LINE INPUT") == 3
    assert "LINE INPUT #1, N$" in lines[0]
    assert "LINE INPUT #1, E$" in lines[0]
    assert "LINE INPUT #1, M$" in lines[0]


def test_def_usr_forbidden():
    lines = ["10 DEF USR0 = 0", "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "DEF USR" in err


def test_open_for_random_rejected_before_parse():
    lines = ['10 OPEN "F" FOR RANDOM AS #1', "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "RANDOM" in err


def test_open_quote_r_rejected():
    lines = ['10 OPEN "R",#1,"F.DAT"', "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "OPEN" in err


def test_get_three_part_rejected():
    lines = ["10 GET #1, 1, N$", "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "GET" in err


def test_field_rejected():
    lines = ["10 FIELD #1, 20 AS N$", "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "FIELD" in err


def test_dim_scalar_rejected():
    lines = ["10 DIM COUNT%", "20 COUNT% = 0", "30 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "DIM" in err and "parentheses" in err.lower()


def test_dim_array_allowed():
    lines = ['10 DIM N$(5)', "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    assert validate_ai_program(lines, ctx) is None


def test_cls_rejected():
    lines = ["10 CLS", "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "CLS" in err


def test_split_rejected():
    lines = ['10 SPLIT A$ BY "," INTO B$, C$', "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    err = validate_ai_program(lines, ctx)
    assert err and "SPLIT" in err


def test_suffix_mismatch():
    lines = ["10 A%=1", "20 A!=2", "30 END"]
    assert lint_suffix_consistency(lines)


def test_fix_identical_rejected():
    inp = '10 PRINT "X"\n20 END\n'
    out = ['10 PRINT "X"', "20 END"]
    assert lint_identical_fix(out, inp)


def test_valid_program_passes_parse():
    lines = ['10 PRINT "OK"', "20 END"]
    ctx = ProgramValidationContext("AIBASIC-0.1", _default_def_map(), "generate")
    assert validate_ai_program(lines, ctx) is None


def test_plain_numbered_fallback_without_dialect_field():
    body = '10 PRINT "P"\n20 END\n'
    ok, lines, err = extract_program_from_content(body, "AIBASIC-0.1")
    assert ok and len(lines) == 2 and err is None


def test_fix_failing_line_unchanged_detected():
    inp = '10 PRINT "X"\n20 BADTOKEN\n30 END\n'
    out = ['10 PRINT "X"', "20 BADTOKEN", "30 END"]
    syn = "?Parse error at line 20"
    err = lint_failing_line_unchanged(out, inp, syn)
    assert err and "FAILING LINE" in err
