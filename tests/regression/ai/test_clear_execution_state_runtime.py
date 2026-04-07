"""Regression: clear_execution_state must match Runtime stack fields (not legacy gosub_stack)."""


def test_new_after_run_does_not_raise():
    from src.interactive import InteractiveMode

    m = InteractiveMode()
    m.process_line('10 PRINT "x"')
    m.process_line("20 END")
    m.cmd_run()
    m.cmd_new()
    assert not m.program.lines


def test_aiload_after_run_does_not_raise(monkeypatch):
    from src.interactive import InteractiveMode

    monkeypatch.setenv("TRS_AI_BACKEND", "fixture")
    monkeypatch.delenv("TRS_AI_API_KEY", raising=False)
    m = InteractiveMode()
    m.process_line('10 PRINT "x"')
    m.process_line("20 END")
    m.cmd_run()
    m.cmd_aiload("any prompt")
    assert m.program.lines
