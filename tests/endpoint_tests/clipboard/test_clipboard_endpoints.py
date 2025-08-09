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
