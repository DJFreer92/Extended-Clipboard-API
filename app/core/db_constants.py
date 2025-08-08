from pathlib import Path

# Dirs
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "clipboard.db"
SCHEMA_DIR = BASE_DIR / "app" / "core" / "schema"
QUERIES_DIR = BASE_DIR / "app" / "core" / "queries"
TABLES_DIR = SCHEMA_DIR / "tables"
TRIGGERS_DIR = SCHEMA_DIR / "triggers"
VIEWS_DIR = SCHEMA_DIR / "views"
INDEXES_DIR = SCHEMA_DIR / "indexes"

# Clips
ADD_CLIP = QUERIES_DIR / "add_clip.sql"
GET_N_CLIPS = QUERIES_DIR / "get_n_clips.sql"
