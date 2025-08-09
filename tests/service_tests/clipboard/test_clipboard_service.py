from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from app.services.clipboard import clipboard_service


@pytest.fixture
def fake_rows() -> list[dict[str, Any]]:
    return [
        {"id": 1, "content": "alpha", "timestamp": "2025-01-01T00:00:00Z"},
        {"id": 2, "content": "beta", "timestamp": "2025-01-02T00:00:00Z"},
    ]


def test_get_recent_clips_maps_rows_to_model(fake_rows: list[dict[str, Any]]):
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=fake_rows) as exec_mock:
        result = clipboard_service.get_recent_clips(2)
        exec_mock.assert_called_once()
        assert len(result.clips) == 2
        assert result.clips[0].id == 1
        assert result.clips[0].content == "alpha"


def test_get_all_clips_maps_rows_to_model(fake_rows: list[dict[str, Any]]):
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=fake_rows) as exec_mock:
        result = clipboard_service.get_all_clips()
        exec_mock.assert_called_once()
        assert len(result.clips) == 2
        assert result.clips[1].id == 2
        assert result.clips[1].content == "beta"


def test_add_clip_calls_execute_query():
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_mock:
        clipboard_service.add_clip("hello world")
        exec_mock.assert_called_once()
        args, kwargs = exec_mock.call_args
        assert ("hello world",) in args or kwargs.get("params") == ("hello world",)


def test_delete_clip_calls_execute_query():
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_mock:
        clipboard_service.delete_clip(123)
        exec_mock.assert_called_once()
        args, kwargs = exec_mock.call_args
        assert (123,) in args or kwargs.get("params") == (123,)


def test_delete_all_clips_calls_execute_query():
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_mock:
        clipboard_service.delete_all_clips()
        exec_mock.assert_called_once()
