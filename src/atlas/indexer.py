from sqlite3 import Connection
import time


def upsert_files(conn: Connection, file_records: dict, scanned_at: int = None):
    scanned_at = scanned_at or int(time.time())
    count = 0

    query = """
        INSERT INTO files (root, path, folder, name, extension, size_bytes, modified_at, created_at, scanned_at)
        VALUES (:root, :path, :folder, :name, :extension, :size_bytes, :modified_at, :created_at, :scanned_at)
        ON CONFLICT(path) DO UPDATE SET
            size_bytes  = excluded.size_bytes,
            modified_at = excluded.modified_at,
            scanned_at  = excluded.scanned_at
    """

    for f in file_records:
        params = {**f, "scanned_at": scanned_at}
        conn.execute(query, params)
        count += 1

    conn.commit()
    return count


def oldest_files(conn: Connection, limit: int = 20):
    query = """
        SELECT 
            name,
            root,
            path,
            folder,
            extension,
            size_bytes,
            modified_at,
            created_at,
            scanned_at
        FROM files 
        ORDER BY modified_at ASC 
        LIMIT ?
    """

    params = (limit, )
    result = conn.execute(query, params)

    return result.fetchall()
