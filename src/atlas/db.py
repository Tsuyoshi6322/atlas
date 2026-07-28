import sqlite3


DB_PATH = "atlas_index.db"


def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            root TEXT NOT NULL,
            path TEXT UNIQUE NOT NULL,
            folder TEXT,
            name TEXT,
            extension TEXT,
            size_bytes INTEGER,
            modified_at INTEGER,
            scanned_at INTEGER
        )
    """)
    conn.commit()
