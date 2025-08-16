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
GET_ALL_FROM_APPS: Path = QUERIES_DIR / "get_all_from_apps.sql"
GET_LAST_CLIP_ID: Path = QUERIES_DIR / "get_last_clip_id.sql"

# Tags & Favorites
ADD_CLIP_TAG: Path = QUERIES_DIR / "add_clip_tag.sql"
ADD_TAG_IF_NOT_EXISTS: Path = QUERIES_DIR / "add_tag_if_not_exists.sql"
REMOVE_CLIP_TAG: Path = QUERIES_DIR / "remove_clip_tag.sql"
GET_ALL_TAGS: Path = QUERIES_DIR / "get_all_tags.sql"
GET_NUM_CLIPS_PER_TAG: Path = QUERIES_DIR / "get_num_clips_per_tag.sql"
ADD_FAVORITE: Path = QUERIES_DIR / "add_favorite.sql"
REMOVE_FAVORITE: Path = QUERIES_DIR / "remove_favorite.sql"
GET_ALL_FAVORITES: Path = QUERIES_DIR / "get_all_favorites.sql"
GET_NUM_FAVORITES: Path = QUERIES_DIR / "get_num_favorites.sql"

# Deletion helpers (single-statement)
DELETE_FAVORITE_FOR_CLIP: Path = QUERIES_DIR / "delete_favorite_for_clip.sql"
GET_TAG_IDS_FOR_CLIP: Path = QUERIES_DIR / "get_tag_ids_for_clip.sql"
DELETE_CLIP_TAGS_FOR_CLIP: Path = QUERIES_DIR / "delete_clip_tags_for_clip.sql"
DELETE_UNUSED_TAG: Path = QUERIES_DIR / "delete_unused_tag.sql"
DELETE_ALL_CLIP_TAGS: Path = QUERIES_DIR / "delete_all_clip_tags.sql"
DELETE_ALL_FAVORITES: Path = QUERIES_DIR / "delete_all_favorites.sql"
DELETE_ALL_TAGS: Path = QUERIES_DIR / "delete_all_tags.sql"
