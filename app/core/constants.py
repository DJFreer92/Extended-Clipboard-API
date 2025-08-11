from pathlib import Path

# Dirs
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
APP_DIR: Path = BASE_DIR / "app"
SCHEMA_DIR: Path = APP_DIR / "db" / "schema"
QUERIES_DIR: Path = APP_DIR / "db" / "queries"
TABLES_DIR: Path = SCHEMA_DIR / "tables"
TRIGGERS_DIR: Path = SCHEMA_DIR / "triggers"
VIEWS_DIR: Path = SCHEMA_DIR / "views"
INDEXES_DIR: Path = SCHEMA_DIR / "indexes"

# DB
DB_PATH: Path = APP_DIR / "db" / "clipboard.db"

# Clips
ADD_CLIP: Path = QUERIES_DIR / "add_clip.sql"
GET_N_CLIPS: Path = QUERIES_DIR / "get_n_clips.sql"
GET_ALL_CLIPS: Path = QUERIES_DIR / "get_all_clips.sql"
DELETE_CLIP: Path = QUERIES_DIR / "delete_clip.sql"
DELETE_ALL_CLIPS: Path = QUERIES_DIR / "delete_all_clips.sql"
ADD_CLIP_WITH_TIMESTAMP: Path = QUERIES_DIR / "add_clip_with_timestamp.sql"
GET_ALL_CLIPS_AFTER_ID: Path = QUERIES_DIR / "get_all_clips_after_id.sql"
GET_N_CLIPS_BEFORE_ID: Path = QUERIES_DIR / "get_n_clips_before_id.sql"
GET_NUM_CLIPS: Path = QUERIES_DIR / "get_num_clips.sql"
