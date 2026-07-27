from pathlib import Path
import os

from atlas.exclusions import ExclusionRules


def scan_folder(root_path: str, rules: ExclusionRules, skipped_counter: int):
    for entry in os.scandir(root_path):
        try:
            if entry.is_dir(follow_symlinks = False):
                if rules.is_folder_excluded(entry.name, entry.path):
                    skipped_counter[0] += 1
                    continue
                yield from scan_folder(entry.path, rules, skipped_counter)

            elif entry.is_file(follow_symlinks = False):
                if rules.is_file_excluded(entry.name):
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
