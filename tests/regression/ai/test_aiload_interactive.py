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
        def generate(self, prompt, dialect_spec):
            from src.trs_ai.types import GenerationResult

            return GenerationResult(ok=True, lines=["not a numbered line"])

    monkeypatch.setattr(
        "src.trs_ai.backends.load_backend_from_env", lambda: BadBackend()
    )
    monkeypatch.setattr(sys, "stdout", StringIO())
    im.execute_immediate('AILOAD "x"')
    assert 10 in im.program.lines
    assert "KEEP" in im.program.lines[10]
