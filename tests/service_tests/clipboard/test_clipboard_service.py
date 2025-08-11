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
        # Accept both positional and keyword param passing styles
        positional_dict = (
            len(args) >= 2 and isinstance(args[1], dict) and args[1].get("content") == "hello world"
        )
        kw_params = kwargs.get("params")
        assert (
            ("hello world",) in args
            or kw_params == ("hello world",)
            or kw_params == {"content": "hello world"}
            or (isinstance(kw_params, dict) and kw_params.get("content") == "hello world")
            or positional_dict
        )


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


# ---- Merged tests from test_new_service.py ----


def test_get_all_clips_after_id_calls_execute_query():
    from app.services.clipboard import clipboard_service as svc

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[(3, "c", "t")]) as exec_q:
        result = svc.get_all_clips_after_id(2)
        exec_q.assert_called_once()
        assert result.clips[0].id == 3


def test_get_n_clips_before_id_calls_execute_query():
    from app.services.clipboard import clipboard_service as svc

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[(2, "b", "t")]) as exec_q:
        result = svc.get_n_clips_before_id(1, 3)
        exec_q.assert_called_once()
        assert result.clips[0].id == 2


def test_get_num_clips_calls_execute_query():
    from app.services.clipboard import clipboard_service as svc

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[(5,)]) as exec_q:
        count = svc.get_num_clips()
        exec_q.assert_called_once()
        assert count == 5


def test_add_clip_with_timestamp_calls_execute_query():
    from app.services.clipboard import clipboard_service as svc

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_q:
        svc.add_clip_with_timestamp("x", "2024-01-01 00:00:00")
        exec_q.assert_called_once()


def test_dynamic_filters_use_execute_dynamic_query():
    from app.services.clipboard import clipboard_service as svc

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(1, "a", "t")]) as exec_d:
        out = svc.filter_all_clips("a", "")
        exec_d.assert_called()
        assert out.clips[0].content == "a"

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(1, "a", "t")]) as exec_d:
        out = svc.filter_n_clips("a", "", 1)
        exec_d.assert_called()

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(2, "b", "t")]) as exec_d:
        out = svc.filter_all_clips_after_id("", "", 1)
        exec_d.assert_called()
        assert out.clips[0].id == 2

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(3, "c", "t")]) as exec_d:
        out = svc.filter_n_clips_before_id("", "", 1, 4)
        exec_d.assert_called()
        assert out.clips[0].id == 3

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(7,)]) as exec_d:
        count = svc.get_num_filtered_clips("", "")
        exec_d.assert_called()
        assert count == 7
