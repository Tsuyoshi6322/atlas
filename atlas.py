import os
import sqlite3
import time
import json
import fnmatch
from pathlib import Path

DB_PATH = "atlas_index.db"
CONFIG_PATH = "atlas_config.json"

DEFAULT_CONFIG = {
    "excluded_folder_names": [
        "node_modules", ".git", "__pycache__",
        "$RECYCLE.BIN", "System Volume Information"
    ],
    "excluded_paths": [
        "C:\\Windows", "C:\\ProgramData",
        "C:\\Program Files", "C:\\Program Files (x86)"
    ],
    "excluded_file_patterns": [
        "Thumbs.db", "desktop.ini", "~$*", "*.tmp", "*.log"
    ]
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        print(f"Created default config at {CONFIG_PATH} — edit it to adjust exclusions.")
        return DEFAULT_CONFIG
    with open(CONFIG_PATH) as f:
        return json.load(f)

def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
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

def scan_folder(root_path, config, skipped_counter):
    excluded_names = {n.lower() for n in config["excluded_folder_names"]}
    excluded_paths = [p.lower() for p in config["excluded_paths"]]
    excluded_patterns = config["excluded_file_patterns"]

    for entry in os.scandir(root_path):
        try:
            entry_path_lower = entry.path.lower()

            if entry.is_dir(follow_symlinks=False):
                if entry.name.lower() in excluded_names:
                    skipped_counter[0] += 1
                    continue
                if any(entry_path_lower.startswith(p) for p in excluded_paths):
                    skipped_counter[0] += 1
                    continue
                yield from scan_folder(entry.path, config, skipped_counter)

            elif entry.is_file(follow_symlinks=False):
                if any(fnmatch.fnmatch(entry.name.lower(), pat.lower()) for pat in excluded_patterns):
                    skipped_counter[0] += 1
                    continue
                stat = entry.stat()
                yield {
                    "path": entry.path,
                    "folder": str(Path(entry.path).parent),
                    "name": entry.name,
                    "extension": Path(entry.name).suffix.lower(),
                    "size_bytes": stat.st_size,
                    "modified_at": int(stat.st_mtime),
                }
        except PermissionError:
            print(f"Skipped (no permission): {entry.path}")
        except OSError as e:
            print(f"Skipped ({e}): {entry.path}")

def main(root_folder):
    config = load_config()
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    now = int(time.time())
    count = 0
    skipped = [0]

    for f in scan_folder(root_folder, config, skipped):
        conn.execute("""
            INSERT INTO files (path, folder, name, extension, size_bytes, modified_at, scanned_at)
            VALUES (:path, :folder, :name, :extension, :size_bytes, :modified_at, :scanned_at)
            ON CONFLICT(path) DO UPDATE SET
                size_bytes=excluded.size_bytes,
                modified_at=excluded.modified_at,
                scanned_at=excluded.scanned_at
        """, {**f, "scanned_at": now})
        count += 1
    conn.commit()

    print(f"Scanned {count} files from {root_folder}")
    print(f"Skipped {skipped[0]} excluded folders/files")

    print("\nTop 20 oldest-modified files (likely forgotten):")
    for row in conn.execute(
        "SELECT path, size_bytes, modified_at FROM files ORDER BY modified_at ASC LIMIT 20"
    ):
        print(row)

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
