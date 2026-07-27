import sys

from atlas.config import load_config
from atlas.exclusions import ExclusionRules
from atlas.scanner import scan_folder
from atlas.db import get_connection
from atlas.indexer import upsert_files, oldest_files


def main(root_folder = "."):
    config = load_config()
    rules = ExclusionRules(config)
    conn = get_connection()

    skipped = [0]
    records = scan_folder(root_folder, rules, skipped)
    count = upsert_files(conn, records)

    print(f"Scanned {count} files from {root_folder}")
    print(f"Skipped {skipped[0]} excluded folders/files")

    print("\nTop 20 oldest-modified files (likely forgotten):")
    for row in oldest_files(conn):
        print(row)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
