from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pytest

from app.db.db import execute_query, init_db
from app.core.constants import (
    ADD_CLIP,
    GET_ALL_CLIPS,
    GET_N_CLIPS,
    DELETE_CLIP,
    DELETE_ALL_CLIPS,
)


@pytest.fixture
def temp_db(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[None]:
    """Point DB_PATH to a temp SQLite file and initialize real schema/triggers."""
    import app.db.db as dbmod

    tmp_db = tmp_path / "test_clipboard.db"
    monkeypatch.setattr(dbmod, "DB_PATH", tmp_db, raising=False)
    init_db()
    yield


def test_add_clip_and_get_all_returns_inserted_row(temp_db: None) -> None:
    execute_query(ADD_CLIP, {"content": "alpha"})

    rows = execute_query(GET_ALL_CLIPS)
    assert len(rows) == 1
    assert rows[0][1] == "alpha"


def test_get_n_clips_orders_desc_and_limits(temp_db: None) -> None:
    for content in ("a", "b", "c"):
        execute_query(ADD_CLIP, {"content": content})

    rows = execute_query(GET_N_CLIPS, {"n": 2})
    assert len(rows) == 2
    contents = [r[1] for r in rows]
    assert contents == ["c", "b"]


def test_delete_clip_removes_only_that_row(temp_db: None) -> None:
    execute_query(ADD_CLIP, {"content": "first"})
    execute_query(ADD_CLIP, {"content": "second"})

    all_rows = execute_query(GET_ALL_CLIPS)
    first_row = next(r for r in all_rows if r[1] == "first")
    first_id = first_row[0]

    execute_query(DELETE_CLIP, (first_id,))

    remaining = execute_query(GET_ALL_CLIPS)
    assert [r[1] for r in remaining] == ["second"]


def test_delete_all_clips_clears_table(temp_db: None) -> None:
    for content in ("x", "y"):
        execute_query(ADD_CLIP, {"content": content})

    execute_query(DELETE_ALL_CLIPS)
    assert len(execute_query(GET_ALL_CLIPS)) == 0
