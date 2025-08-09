import sqlite3
from app.core.db_constants import *

def get_connection() -> sqlite3.Connection:
    """Returns a new SQLite connection to the persistent clipboard.db file."""
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    if Path(DB_PATH).exists():
        print("Database already exists. Skipping init.")
        return

    with get_connection() as conn:
        for subdir in ["tables", "indexes", "triggers", "views"]:
            dir_path: Path = Path(SCHEMA_DIR) / subdir
            for sql_file in sorted(dir_path.glob("*.sql")):
                with open(sql_file, "r", encoding="utf-8") as f:
                    print(f"Running schema: {sql_file.name}")
                    conn.executescript(f.read())
        conn.commit()
        print(f"Database created at {DB_PATH}")

def execute_query(filename: str, params: tuple | dict | None = None):
    """Loads a SQL query from file and executes it with optional parameters."""
    query_path: Path = Path(QUERIES_DIR) / filename
    if not query_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_path}")

    sql: str = query_path.read_text(encoding="utf-8")

    with get_connection() as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(sql, params or ())
        results: list = cursor.fetchall()
        return results
