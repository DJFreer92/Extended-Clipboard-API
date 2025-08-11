from __future__ import annotations

from pathlib import Path
from typing import Iterator
import re

import pytest

from app.db.db import execute_query, execute_dynamic_query, init_db
from app.core.constants import (
    ADD_CLIP,
    ADD_CLIP_WITH_TIMESTAMP,
    GET_ALL_CLIPS,
    GET_N_CLIPS,
    GET_ALL_CLIPS_AFTER_ID,
    GET_N_CLIPS_BEFORE_ID,
    GET_NUM_CLIPS,
    DELETE_CLIP,
    DELETE_ALL_CLIPS,
)
from app.db.queries.filter_clips_dynamic_queries import (
    filter_all_clips_query,
    filter_n_clips_query,
    filter_all_clips_after_id_query,
    filter_n_clips_before_id_query,
    get_num_filtered_clips_query,
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


# ---- Merged tests from test_new_queries.py ----

def _insert_many(contents: list[str]):
    for c in contents:
        execute_query(ADD_CLIP, {"content": c})


def test_static_queries_after_before_and_count(temp_db: None):
    _insert_many(["a", "b", "c", "d"])  # IDs 1..4

    after_rows = execute_query(GET_ALL_CLIPS_AFTER_ID, {"before_id": 2})
    assert [r[1] for r in after_rows] == ["d", "c"]

    before_rows = execute_query(GET_N_CLIPS_BEFORE_ID, {"before_id": 4, "n": 2})
    assert [r[1] for r in before_rows] == ["c", "b"]

    count_rows = execute_query(GET_NUM_CLIPS)
    assert count_rows[0][0] == 4


def test_dynamic_filter_queries(temp_db: None):
    _insert_many(["alpha beta", "beta gamma", "delta", "epsilon alpha"])  # 4 rows

    # filter all with keyword alpha
    rows = execute_dynamic_query(lambda: filter_all_clips_query(search="alpha", time_frame=""))
    assert len(rows) == 2

    # filter n with n=1
    rows = execute_dynamic_query(lambda: filter_n_clips_query(search="beta", time_frame="", n=1))
    assert len(rows) == 1

    # after_id
    rows = execute_dynamic_query(lambda: filter_all_clips_after_id_query(search="", time_frame="", after_id=2))
    assert len(rows) == 2

    # before_id with limit 1
    rows = execute_dynamic_query(
        lambda: filter_n_clips_before_id_query(search="", time_frame="", before_id=4, n=1)
    )
    assert len(rows) == 1

    # count filtered
    rows = execute_dynamic_query(lambda: get_num_filtered_clips_query(search="beta", time_frame=""))
    assert rows[0][0] == 2


def test_add_clip_with_timestamp(temp_db: None):
    execute_query(ADD_CLIP_WITH_TIMESTAMP, {"content": "ts-test", "timestamp": "2024-01-01 12:00:00"})
    rows = execute_query(GET_ALL_CLIPS)
    assert rows[0][1] == "ts-test"
    # SQLite stores timestamps as strings in this schema; check format looks right
    assert re.match(r"\d{4}-\d{2}-\d{2} ", rows[0][2])
