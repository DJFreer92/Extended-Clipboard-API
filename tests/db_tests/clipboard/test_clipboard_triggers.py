from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pytest

from app.db.db import execute_query, init_db
from app.core.constants import ADD_CLIP, GET_ALL_CLIPS


@pytest.fixture
def temp_db(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[None]:
    import app.db.db as dbmod

    tmp_db = tmp_path / "test_clipboard.db"
    monkeypatch.setattr(dbmod, "DB_PATH", tmp_db, raising=False)
    init_db()
    yield


def test_trigger_delete_old_if_duplicate_keeps_single_latest_row(temp_db: None) -> None:
    execute_query(ADD_CLIP, {"content": "dup"})
    execute_query(ADD_CLIP, {"content": "dup"})

    rows = execute_query(GET_ALL_CLIPS)
    assert len(rows) == 1
    only_row = rows[0]
    assert only_row[1] == "dup"
    assert only_row[0] == 2
