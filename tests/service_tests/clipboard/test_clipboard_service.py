from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from app.services.clipboard import clipboard_service


@pytest.fixture
def fake_rows() -> list[dict[str, Any]]:
    return [
    {"ClipID": 1, "Content": "alpha", "FromAppName": "AppA", "Tags": "x,y", "Timestamp": "2025-01-01T00:00:00Z", "IsFavorite": 1},
    {"ClipID": 2, "Content": "beta", "FromAppName": None, "Tags": None, "Timestamp": "2025-01-02T00:00:00Z", "IsFavorite": 0},
    ]


@pytest.fixture
def fake_rows_sqlite_format() -> list[dict[str, Any]]:
    # Simulate SQLite datetime format without timezone info
    return [
    {"ClipID": 1, "Content": "alpha", "FromAppName": "AppA", "Tags": "x,y", "Timestamp": "2025-01-01 00:00:00", "IsFavorite": 1},
    {"ClipID": 2, "Content": "beta", "FromAppName": None, "Tags": None, "Timestamp": "2025-01-02 12:30:45", "IsFavorite": 0},
    ]


def test_get_recent_clips_maps_rows_to_model(fake_rows: list[dict[str, Any]]):
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=fake_rows) as exec_mock:
        result = clipboard_service.get_recent_clips(2)
        exec_mock.assert_called_once()
        assert len(result.clips) == 2
        assert result.clips[0].id == 1
        assert result.clips[0].content == "alpha"
        assert result.clips[0].from_app_name == "AppA"
    assert result.clips[0].tags == ["x", "y"]
    assert result.clips[0].is_favorite is True


def test_get_recent_clips_converts_sqlite_timestamps_to_utc_format(fake_rows_sqlite_format: list[dict[str, Any]]):
    """Test that SQLite datetime format gets converted to UTC with Z suffix."""
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=fake_rows_sqlite_format) as exec_mock:
        result = clipboard_service.get_recent_clips(2)
        exec_mock.assert_called_once()
        assert len(result.clips) == 2
        # Timestamps should be converted to UTC format with Z suffix
        assert result.clips[0].timestamp == "2025-01-01T00:00:00Z"
        assert result.clips[1].timestamp == "2025-01-02T12:30:45Z"


def test_get_all_clips_maps_rows_to_model(fake_rows: list[dict[str, Any]]):
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=fake_rows) as exec_mock:
        result = clipboard_service.get_all_clips()
        exec_mock.assert_called_once()
        assert len(result.clips) == 2
        assert result.clips[1].id == 2
        assert result.clips[1].content == "beta"


def test_add_clip_calls_execute_query():
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_mock:
        clipboard_service.add_clip("hello world", from_app_name="AppSrc")
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
        # multiple calls now for composed deletion logic; ensure last call deletes clip
        assert exec_mock.call_count >= 2
        last_call = exec_mock.call_args_list[-1]
        args, kwargs = last_call
        # Expect DELETE_CLIP file path then params dict
        assert any(
            (isinstance(a, dict) and a.get("clip_id") == 123)
            or (isinstance(kwargs.get("params"), dict) and kwargs.get("params").get("clip_id") == 123)
            for a in args
        ) or (kwargs.get("clip_id") == 123)


def test_delete_all_clips_calls_execute_query():
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_mock:
        clipboard_service.delete_all_clips()
        assert exec_mock.call_count == 4


def test_add_clip_with_timestamp_support_uses_provided_timestamp():
    """Test that add_clip_with_timestamp_support properly handles provided UTC timestamps."""
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_mock:
        clipboard_service.add_clip_with_timestamp_support(
            content="test content",
            timestamp="2025-01-01T15:30:00Z",
            from_app_name="TestApp"
        )
        exec_mock.assert_called_once()
        args, kwargs = exec_mock.call_args
        # Should use ADD_CLIP_WITH_TIMESTAMP and convert timestamp to SQLite format
        query_params = args[1] if len(args) >= 2 else kwargs.get("params")
        assert query_params["content"] == "test content"
        assert query_params["timestamp"] == "2025-01-01 15:30:00"  # Converted to SQLite format
        assert query_params["from_app_name"] == "TestApp"


def test_add_clip_with_timestamp_support_generates_utc_when_no_timestamp():
    """Test that add_clip_with_timestamp_support generates UTC timestamp when none provided."""
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_mock:
        with patch("app.services.clipboard.clipboard_service._generate_utc_timestamp", return_value="2025-08-15T12:00:00Z") as time_mock:
            clipboard_service.add_clip_with_timestamp_support(
                content="test content",
                timestamp=None,
                from_app_name="TestApp"
            )
            time_mock.assert_called_once()
            exec_mock.assert_called_once()
            args, kwargs = exec_mock.call_args
            query_params = args[1] if len(args) >= 2 else kwargs.get("params")
            assert query_params["timestamp"] == "2025-08-15 12:00:00"  # Converted to SQLite format


# ---- Merged tests from test_new_service.py ----


def test_ensure_utc_format_handles_various_inputs():
    """Test _ensure_utc_format helper function with different timestamp formats."""
    from app.services.clipboard.clipboard_service import _ensure_utc_format

    # Already UTC format with Z
    assert _ensure_utc_format("2025-01-01T12:00:00Z") == "2025-01-01T12:00:00Z"

    # SQLite datetime format (space-separated)
    assert _ensure_utc_format("2025-01-01 12:00:00") == "2025-01-01T12:00:00Z"

    # ISO format without Z
    assert _ensure_utc_format("2025-01-01T12:00:00") == "2025-01-01T12:00:00Z"


def test_parse_timestamp_for_db_converts_utc_to_sqlite_format():
    """Test _parse_timestamp_for_db helper function."""
    from app.services.clipboard.clipboard_service import _parse_timestamp_for_db

    # UTC timestamp with Z should become SQLite format
    assert _parse_timestamp_for_db("2025-01-01T12:00:00Z") == "2025-01-01 12:00:00"

    # ISO without Z should become SQLite format
    assert _parse_timestamp_for_db("2025-01-01T12:00:00") == "2025-01-01 12:00:00"

    # Already SQLite format should remain unchanged
    assert _parse_timestamp_for_db("2025-01-01 12:00:00") == "2025-01-01 12:00:00"


def test_generate_utc_timestamp_returns_utc_with_z_suffix():
    """Test _generate_utc_timestamp returns proper UTC format."""
    from app.services.clipboard.clipboard_service import _generate_utc_timestamp

    timestamp = _generate_utc_timestamp()
    assert timestamp.endswith("Z")
    assert "T" in timestamp
    # Should be in ISO format like "2025-08-15T12:34:56Z"
    import re
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp)


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
        svc.add_clip_with_timestamp("x", "2024-01-01 00:00:00", from_app_name="Src")
        exec_q.assert_called_once()


def test_dynamic_filters_use_execute_dynamic_query():
    from app.services.clipboard import clipboard_service as svc

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(1, "a", None, "x,y", "t", 1)]) as exec_d:
        out = svc.filter_all_clips("a", "", ["x"], [], True)
        exec_d.assert_called()
        assert out.clips[0].content == "a"
        assert out.clips[0].is_favorite is True

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(1, "a", None, None, "t", 0)]) as exec_d:
        out = svc.filter_n_clips("a", "", 1, ["x"], [], False)
        exec_d.assert_called()

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(2, "b", None, None, "t", 0)]) as exec_d:
        out = svc.filter_all_clips_after_id("", "", 1, [], [], False)
        exec_d.assert_called()
        assert out.clips[0].id == 2

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(3, "c", None, None, "t", 0)]) as exec_d:
        out = svc.filter_n_clips_before_id("", "", 1, 4, [], [], False)
        exec_d.assert_called()
        assert out.clips[0].id == 3

    with patch("app.services.clipboard.clipboard_service.execute_dynamic_query", return_value=[(7,)]) as exec_d:
        count = svc.get_num_filtered_clips("", "", [], [], False)
        exec_d.assert_called()
        assert count == 7


def test_tag_and_favorite_methods():
    from app.services.clipboard import clipboard_service as svc

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_q:
        svc.add_clip_tag(1, "tag")
        exec_q.assert_called()

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_q:
        svc.remove_clip_tag(1, 2)
        exec_q.assert_called()

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[(1, "tag")]) as exec_q:
        tags = svc.get_all_tags()
        exec_q.assert_called()
        assert tags.tags[0].name == "tag"

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[(3,)]) as exec_q:
        count = svc.get_num_clips_per_tag(1)
        exec_q.assert_called()
        assert count == 3

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_q:
        svc.add_favorite(5)
        exec_q.assert_called()

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[]) as exec_q:
        svc.remove_favorite(5)
        exec_q.assert_called()

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[(5,), (7,)]) as exec_q:
        favs = svc.get_all_favorites()
        assert favs.clip_ids == [5, 7]

    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[(10,)]) as exec_q:
        fav_count = svc.get_num_favorites()
        assert fav_count == 10


def test_get_all_from_apps():
    from app.services.clipboard import clipboard_service as svc
    with patch("app.services.clipboard.clipboard_service.execute_query", return_value=[("Chrome",), ("Safari",), (None,)]) as exec_q:
        apps = svc.get_all_from_apps()
        exec_q.assert_called_once()
        assert set(apps) == {"Chrome", "Safari"}
