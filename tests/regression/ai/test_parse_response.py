"""TRS-AI: parse model output into BASIC lines."""

import json

import pytest

from src.trs_ai.parse_response import (
    lines_from_parsed_json,
    parse_assistant_content,
    strip_markdown_fences,
)


def test_strip_markdown_fences_json():
    raw = '```json\n{"a": 1}\n```'
    assert strip_markdown_fences(raw).startswith("{")


def test_lines_from_parsed_json_ok():
    data = json.loads(
        '{"dialect": "AIBASIC-0.1", "program": ["10 PRINT \\"X\\"", "20 END"]}'
    )
    ok, lines, err = lines_from_parsed_json(data)
    assert ok
    assert lines == ['10 PRINT "X"', "20 END"]
    assert err is None


def test_lines_from_parsed_json_missing_program():
    ok, lines, err = lines_from_parsed_json({"dialect": "x"})
    assert not ok
    assert "program" in (err or "")


def test_parse_assistant_content_json():
    body = json.dumps(
        {"dialect": "AIBASIC-0.1", "program": ['10 PRINT "HI"', "20 END"]}
    )
    ok, lines, err = parse_assistant_content(body)
    assert ok
    assert "PRINT" in lines[0]


def test_parse_assistant_content_plain_numbered():
    text = "100 LET A=1\n110 END\n"
    ok, lines, err = parse_assistant_content(text)
    assert ok
    assert lines == ["100 LET A=1", "110 END"]


def test_parse_assistant_content_empty():
    ok, lines, err = parse_assistant_content("   ")
    assert not ok


@pytest.mark.parametrize(
    "content",
    [
        '```\n10 PRINT "A"\n```',
        '```json\n{"dialect":"x","program":["10 PRINT \\"A\\""]}\n```',
    ],
)
def test_parse_assistant_content_fenced(content):
    ok, lines, err = parse_assistant_content(content)
    assert ok
    assert any("PRINT" in ln for ln in lines)
