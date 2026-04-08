"""Milestone 3: AIMERGE, AIFIX, AIDIFF, AIAPPLY, AICANCEL, AIEXPLAIN, pending buffer."""

from __future__ import annotations

import os

import pytest

from src.interactive import InteractiveMode
from src.trs_ai.program_diff import line_numbered_program_diff


@pytest.fixture
def fixture_env(monkeypatch):
    monkeypatch.setenv("TRS_AI_BACKEND", "fixture")
    monkeypatch.delenv("TRS_AI_API_KEY", raising=False)


def test_program_diff_by_line_number():
    cur = {10: "10 N=5", 20: "20 PRINT N"}
    pend = {10: "10 N=5", 20: "20 N=RND(10)", 25: "25 C=0"}
    rows = line_numbered_program_diff(cur, pend)
    assert "- 20 PRINT N" in rows
    assert "+ 20 N=RND(10)" in rows
    assert "+ 25 C=0" in rows


def test_aimerge_accumulates_on_pending(fixture_env):
    m = InteractiveMode()
    m.process_line('10 PRINT "HI"')
    m.process_line("20 END")
    m.cmd_aimerge("first")
    first = dict(m.ai_pending_lines or {})
    assert first
    m.cmd_aimerge("second")
    second = m.ai_pending_lines or {}
    assert second != first or any("AIMERGE" in second[k] for k in second)


def test_aiapply_aicancel(fixture_env, capsys):
    m = InteractiveMode()
    m.process_line("10 REM BASE")
    m.cmd_aimerge("change")
    assert m.ai_pending_lines
    m.cmd_aicancel()
    out = capsys.readouterr().out
    assert "AI CHANGES CANCELED" in out
    assert m.ai_pending_lines is None

    m.cmd_aimerge("again")
    m.cmd_aiapply()
    assert m.ai_pending_lines is None
    assert any("AIMERGE" in m.lines[k] for k in m.lines)


def test_aiload_clears_pending(fixture_env):
    m = InteractiveMode()
    m.process_line("10 REM OLD")
    m.cmd_aimerge("edit")
    assert m.ai_pending_lines
    m.cmd_aiload("fresh")
    assert m.ai_pending_lines is None
    assert any("AILOAD_OK" in m.lines[k] for k in m.lines)


def test_no_program_aimerge_aifix(fixture_env, capsys):
    m = InteractiveMode()
    m.cmd_aimerge("x")
    assert "NO PROGRAM IN MEMORY" in capsys.readouterr().out
    m.cmd_aifix(None)
    assert "NO PROGRAM IN MEMORY" in capsys.readouterr().out


def test_manual_edit_discards_pending(fixture_env, capsys):
    m = InteractiveMode()
    m.process_line("10 X=1")
    m.cmd_aimerge("z")
    m.process_line("20 Y=2")
    out = capsys.readouterr().out
    assert "PENDING AI CHANGES DISCARDED DUE TO MANUAL EDIT" in out
    assert m.ai_pending_lines is None


def test_aidiff_no_pending(fixture_env, capsys):
    m = InteractiveMode()
    m.cmd_aidiff()
    assert "NO PENDING AI CHANGES" in capsys.readouterr().out


def test_parse_explanation_content_json():
    from src.trs_ai.parse_response import parse_explanation_content

    ok, text, err = parse_explanation_content('{"explanation": "hello"}')
    assert ok and text == "hello" and err is None


@pytest.mark.skipif(
    not os.environ.get("TRS_AI_RUN_LIVE"),
    reason="Set TRS_AI_RUN_LIVE=1 and TRS_AI_API_KEY for live M3 smoke",
)
def test_live_remote_merge_smoke():
    """Optional real API check for merge path."""
    os.environ["TRS_AI_BACKEND"] = "remote"
    if not os.environ.get("TRS_AI_API_KEY"):
        pytest.skip("TRS_AI_API_KEY not set")
    m = InteractiveMode()
    m.process_line('10 PRINT "LIVE"')
    m.process_line("20 END")
    m.cmd_aimerge("Add a REM line at the end describing the program")
    assert m.ai_pending_lines
    m.cmd_aicancel()
