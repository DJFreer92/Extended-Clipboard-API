from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api.main import app
from app.models.clipboard.clipboard_models import Clip, Clips


client = TestClient(app)


def test_get_recent_clips_endpoint_returns_clips_json():
    fake = Clips(
        clips=[
            Clip(id=1, content="a", timestamp="2025-01-01T00:00:00Z"),
            Clip(id=2, content="b", timestamp="2025-01-02T00:00:00Z"),
        ]
    )

    with patch(
        "app.api.clipboard.clipboard_endpoints.clipboard_service.get_recent_clips",
        return_value=fake,
    ) as mock_get:
        resp = client.get("/clipboard/get_recent_clips", params={"n": 2})
        assert resp.status_code == 200
        data = resp.json()
        assert "clips" in data and len(data["clips"]) == 2
        mock_get.assert_called_once_with(2)


def test_get_all_clips_endpoint_returns_clips_json():
    fake = Clips(
        clips=[
            Clip(id=1, content="a", timestamp="2025-01-01T00:00:00Z"),
        ]
    )

    with patch(
        "app.api.clipboard.clipboard_endpoints.clipboard_service.get_all_clips",
        return_value=fake,
    ) as mock_get:
        resp = client.get("/clipboard/get_all_clips")
        assert resp.status_code == 200
        data = resp.json()
        assert data["clips"][0]["id"] == 1
        mock_get.assert_called_once_with()


def test_add_clip_endpoint_calls_service():
    with patch(
        "app.api.clipboard.clipboard_endpoints.clipboard_service.add_clip",
        return_value=None,
    ) as mock_add:
        body = {"id": 0, "content": "hello", "timestamp": "2025-01-01T00:00:00Z"}
        resp = client.post("/clipboard/add_clip", json=body)
        assert resp.status_code == 200
        mock_add.assert_called_once_with("hello")


def test_delete_clip_endpoint_calls_service():
    with patch(
        "app.api.clipboard.clipboard_endpoints.clipboard_service.delete_clip",
        return_value=None,
    ) as mock_del:
        resp = client.post("/clipboard/delete_clip", params={"id": 123})
        assert resp.status_code == 200
        mock_del.assert_called_once_with(123)


def test_delete_all_clips_endpoint_calls_service():
    with patch(
        "app.api.clipboard.clipboard_endpoints.clipboard_service.delete_all_clips",
        return_value=None,
    ) as mock_del_all:
        resp = client.post("/clipboard/delete_all_clips")
        assert resp.status_code == 200
        mock_del_all.assert_called_once_with()


# ---- Merged tests from test_new_endpoints.py ----


def test_get_all_clips_after_id_endpoint():
    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.get_all_clips_after_id") as m:
        m.return_value = Clips(clips=[])
        resp = client.get("/clipboard/get_all_clips_after_id", params={"before_id": 2})
        assert resp.status_code == 200
        m.assert_called_once_with(2)


def test_get_n_clips_before_id_endpoint():
    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.get_n_clips_before_id") as m:
        m.return_value = Clips(clips=[])
        resp = client.get("/clipboard/get_n_clips_before_id", params={"n": 1, "before_id": 3})
        assert resp.status_code == 200
        m.assert_called_once_with(1, 3)


def test_get_num_clips_endpoint():
    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.get_num_clips", return_value=5) as m:
        resp = client.get("/clipboard/get_num_clips")
        assert resp.status_code == 200
        assert resp.json() == 5
        m.assert_called_once_with()


def test_dynamic_filter_endpoints():
    dummy = Clips(clips=[])

    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.filter_all_clips", return_value=dummy) as m:
        assert client.get("/clipboard/filter_all_clips", params={"search": "a", "time_frame": ""}).status_code == 200
        m.assert_called_once_with("a", "")

    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.filter_n_clips", return_value=dummy) as m:
        assert client.get("/clipboard/filter_n_clips", params={"search": "a", "time_frame": "", "n": 1}).status_code == 200
        m.assert_called_once_with("a", "", 1)

    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.filter_all_clips_after_id", return_value=dummy) as m:
        assert client.get("/clipboard/filter_all_clips_after_id", params={"search": "", "time_frame": "", "after_id": 2}).status_code == 200
        m.assert_called_once_with("", "", 2)

    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.filter_n_clips_before_id", return_value=dummy) as m:
        assert client.get("/clipboard/filter_n_clips_before_id", params={"search": "", "time_frame": "", "n": 1, "before_id": 4}).status_code == 200
        m.assert_called_once_with("", "", 1, 4)

    with patch("app.api.clipboard.clipboard_endpoints.clipboard_service.get_num_filtered_clips", return_value=7) as m:
        resp = client.get("/clipboard/get_num_filtered_clips", params={"search": "", "time_frame": ""})
        assert resp.status_code == 200
        assert resp.json() == 7
        m.assert_called_once_with("", "")
