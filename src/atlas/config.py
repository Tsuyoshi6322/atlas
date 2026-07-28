import json
import os


# Relative to CWD — fine for dev (repo root). 
#   Must become an %APPDATA%-based absolute path 
#   before this ships as a packaged .exe.
CONFIG_PATH = "atlas_config.json"

DEFAULT_CONFIG = {
    "root_folders": ["."],
    "oldest_files_limit": 30,
    "excluded_folder_names": [
        "node_modules", ".git", "__pycache__",
        "$RECYCLE.BIN", "System Volume Information",
        ".vs", "env", ".venv", "venv"
    ],
    "excluded_paths": [
        "C:\\Windows", "C:\\ProgramData",
        "C:\\Program Files", "C:\\Program Files (x86)"
    ],
    "excluded_file_patterns": [
        "Thumbs.db", "desktop.ini", "~$*", "*.tmp", "*.log"
    ]
}


def load_config(path: str = CONFIG_PATH):
    if not os.path.exists(path):
        with open(path, "w") as file: 
            json.dump(DEFAULT_CONFIG, file, indent = 2)

        print(f"Created default config at {path} — edit it to adjust exclusions.")

        return DEFAULT_CONFIG

    with open(path) as file:
        return json.load(file)
