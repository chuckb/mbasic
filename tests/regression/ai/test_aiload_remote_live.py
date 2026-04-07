"""
Optional live HTTP test against a real OpenAI-compatible API.

Enable with: TRS_AI_RUN_LIVE=1 TRS_AI_API_KEY=... pytest ... -k live
"""

import os

import pytest

from src.trs_ai.backends import RemoteChatBackend


@pytest.mark.skipif(
    os.environ.get("TRS_AI_RUN_LIVE", "").strip().lower() not in ("1", "yes", "true"),
    reason="Set TRS_AI_RUN_LIVE=1 to run live AI HTTP test",
)
@pytest.mark.skipif(
    not (os.environ.get("TRS_AI_API_KEY") or "").strip(),
    reason="TRS_AI_API_KEY required for live test",
)
def test_remote_live_hello_world():
    b = RemoteChatBackend(api_key=os.environ["TRS_AI_API_KEY"].strip())
    r = b.generate(
        'Reply with ONLY this JSON and nothing else: '
        '{"dialect":"AIBASIC-0.1","program":["10 PRINT \\"HELLO\\"","20 END"]}',
        "AIBASIC-0.1",
    )
    assert r.ok, r.error
    assert any("HELLO" in ln for ln in r.lines)
