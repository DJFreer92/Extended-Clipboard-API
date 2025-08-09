from pathlib import Path

# Dirs
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DB_PATH: Path = BASE_DIR / "clipboard.db"
SCHEMA_DIR: Path = BASE_DIR / "app" / "core" / "schema"
QUERIES_DIR: Path = BASE_DIR / "app" / "core" / "queries"
TABLES_DIR: Path = SCHEMA_DIR / "tables"
TRIGGERS_DIR: Path = SCHEMA_DIR / "triggers"
VIEWS_DIR: Path = SCHEMA_DIR / "views"
INDEXES_DIR: Path = SCHEMA_DIR / "indexes"

# Clips
ADD_CLIP: Path = QUERIES_DIR / "add_clip.sql"
GET_N_CLIPS: Path = QUERIES_DIR / "get_n_clips.sql"
