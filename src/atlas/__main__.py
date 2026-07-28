import sys
from datetime           import datetime

from atlas.config       import load_config
from atlas.db           import get_connection
from atlas.exclusions   import ExclusionRules
from atlas.indexer      import upsert_files, oldest_files
from atlas.scanner      import scan_folder


def main(root_folder: str = None):
    config = load_config()
    roots = [root_folder] if root_folder else config.get("root_folders", ["."])
    oldest_limit = config.get("oldest_files_limit", 30)

    def format_epoch(timestamp: int) -> str:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    rules = ExclusionRules(config)
    conn = get_connection()

    skipped = [0]
    total_count = 0

    for root in roots:
        records = scan_folder(root, rules, skipped)
        total_count += upsert_files(conn, records)

    print(f"Scanned {total_count} files from {roots}")
    print(f"Skipped {skipped[0]} excluded folders/files")

    print(f"\nTop {oldest_limit} oldest-modified files (likely forgotten):")
    for row in oldest_files(conn, oldest_limit):
        name, root, path, folder, extension, size_bytes, modified_at, created_at, scanned_at = row
        print(f"{name} | {path} | {size_bytes}B | modified={format_epoch(modified_at)} | created={format_epoch(created_at)}")


if __name__ == "__main__":
    cli_arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(cli_arg)
