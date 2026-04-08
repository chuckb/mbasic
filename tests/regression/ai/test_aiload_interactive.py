"""AILOAD through InteractiveMode.execute_immediate (fixture backend)."""

import sys
from io import StringIO

import pytest

from src.interactive import InteractiveMode


@pytest.fixture
def im(monkeypatch):
    monkeypatch.setenv("TRS_AI_BACKEND", "fixture")
    monkeypatch.delenv("TRS_AI_API_KEY", raising=False)
    m = InteractiveMode()
    return m


def test_aiload_loads_fixture_program(im, monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    im.execute_immediate('AILOAD "make anything"')
    out = sys.stdout.getvalue()
    assert "Contacting AI" in out
    assert "Program loaded" in out
    assert 10 in im.program.lines
    assert "AILOAD_OK" in im.program.lines[10]


def test_aiload_rollback_on_bad_lines(im, monkeypatch):
    monkeypatch.setenv("TRS_AI_BACKEND", "fixture")
    im.process_line('10 PRINT "KEEP"')
    im.process_line("20 END")

    class BadBackend:
        def generate(self, prompt, dialect_spec, verbose=False, **kwargs):
            from src.trs_ai.types import GenerationResult

            return GenerationResult(ok=True, lines=["not a numbered line"])

    monkeypatch.setattr(
        "src.trs_ai.backends.load_backend_from_env", lambda: BadBackend()
    )
    monkeypatch.setattr(sys, "stdout", StringIO())
    im.execute_immediate('AILOAD "x"')
    assert 10 in im.program.lines
    assert "KEEP" in im.program.lines[10]
    assert im.ai_pending_lines is not None
    assert -1 in im.ai_pending_lines
    assert "not a numbered" in im.ai_pending_lines[-1]
    assert im.ai_last_syntax_errors


def test_aiload_verbose_emits_fixture_traffic(im, monkeypatch, capsys):
    im.execute_immediate('AILOAD "dbg" VERBOSE')
    out = capsys.readouterr().out
    assert "TRS-AI verbose" in out
    assert "fixture generate (request)" in out
    assert "dbg" in out
    assert "fixture generate (response lines)" in out
    assert "AILOAD_OK" in out


def test_aiload_backend_failure_with_lines_goes_to_pending(im, monkeypatch):
    """M3: failed generation with extractable lines must land in pending for AILIST/AIFIX."""

    class FailWithLines:
        def generate(self, prompt, dialect_spec, verbose=False, **kwargs):
            from src.trs_ai.types import GenerationResult

            return GenerationResult(
                ok=False,
                lines=['10 PRINT "BROKEN {{{"', "20 END"],
                error="AI OUTPUT FAILED PARSE: example",
            )

    monkeypatch.setattr(
        "src.trs_ai.backends.load_backend_from_env", lambda: FailWithLines()
    )
    monkeypatch.setattr(sys, "stdout", StringIO())
    im.execute_immediate('AILOAD "x"')
    assert im.ai_pending_lines is not None
    assert any("BROKEN" in im.ai_pending_lines[k] for k in im.ai_pending_lines)
    assert im.ai_last_syntax_errors
    assert "AILIST OR AIFIX" in sys.stdout.getvalue()
