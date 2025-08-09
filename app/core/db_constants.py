from pathlib import Path

# Dirs
BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)
DB_PATH: str = BASE_DIR + "clipboard.db"
SCHEMA_DIR: str = BASE_DIR + "app" + "core" + "schema"
QUERIES_DIR: str = BASE_DIR + "app" + "core" + "queries"
TABLES_DIR: str = SCHEMA_DIR + "tables"
TRIGGERS_DIR: str = SCHEMA_DIR + "triggers"
VIEWS_DIR: str = SCHEMA_DIR + "views"
INDEXES_DIR: str = SCHEMA_DIR + "indexes"

# Clips
ADD_CLIP: str = QUERIES_DIR + "add_clip.sql"
GET_N_CLIPS: str = QUERIES_DIR + "get_n_clips.sql"
