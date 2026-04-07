"""TRS-AI: RemoteChatBackend with mocked HTTP."""

import json
from unittest.mock import patch

from src.trs_ai.backends import RemoteChatBackend, load_backend_from_env


def _fake_openai_response(content: str) -> bytes:
    payload = {
        "choices": [
            {"message": {"role": "assistant", "content": content}}
        ]
    }
    return json.dumps(payload).encode("utf-8")


class _FakeResponse:
    def __init__(self, body: bytes):
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_remote_chat_backend_json_program():
    inner = json.dumps(
        {"dialect": "AIBASIC-0.1", "program": ['10 PRINT "M"', "20 END"]}
    )

    def fake_urlopen(req, timeout=None):
        return _FakeResponse(_fake_openai_response(inner))

    with patch("urllib.request.urlopen", fake_urlopen):
        b = RemoteChatBackend(api_key="sk-test", base_url="https://example.invalid/v1/chat/completions")
        r = b.generate("x", "AIBASIC-0.1")
    assert r.ok
    assert any("PRINT" in x for x in r.lines)


def test_remote_chat_backend_http_error():
    from urllib.error import HTTPError
    from io import BytesIO

    def boom(*a, **kw):
        raise HTTPError("url", 401, "Unauthorized", hdrs=None, fp=BytesIO(b'{"error":"bad"}'))

    with patch("urllib.request.urlopen", boom):
        b = RemoteChatBackend(api_key="bad")
        r = b.generate("x", "d")
    assert not r.ok
    assert r.error
    assert "401" in r.error


def test_load_backend_from_env_fixture(monkeypatch):
    monkeypatch.delenv("TRS_AI_BACKEND", raising=False)
    monkeypatch.delenv("TRS_AI_API_KEY", raising=False)
    b = load_backend_from_env()
    r = b.generate("any", "d")
    assert r.ok
    assert '10 PRINT "AILOAD_OK"' in r.lines


def test_load_backend_from_env_remote_missing_key(monkeypatch):
    monkeypatch.setenv("TRS_AI_BACKEND", "remote")
    monkeypatch.delenv("TRS_AI_API_KEY", raising=False)
    b = load_backend_from_env()
    r = b.generate("x", "d")
    assert not r.ok
    assert "API_KEY" in (r.error or "")
