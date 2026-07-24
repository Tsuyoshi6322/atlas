# Atlas

[![Static Badge](https://img.shields.io/badge/Solution_Overview-1F6FEB?style=for-the-badge&logo=wikibooks)](../../wiki/Solution-Overview-NEW)
[![Static Badge](https://img.shields.io/badge/MIT_license-grey?style=for-the-badge&logo=googledocs&logoColor=white&labelColor=green)](\LICENSE)
[![Static Badge](https://img.shields.io/badge/Windows-357EC7?style=for-the-badge&logo=https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2FFile%3AWindows_icon_logo.png&logoColor=white&label=platform)](https://github.com/Tsuyoshi6322/atlas#platform)

A local, read-only tool that scans your folders and gives you one honest, sortable view of everything in them - including the files you've forgotten exist.
- No auto-cleanup. 
- No silent moves or deletes. 
- No background actions - it scans on demand.
- Atlas only looks - you decide what to do.


## Why?

Files pile up across Desktop, Downloads, and random project folders with no consistent structure, and there's no easy way to see what's actually there without opening every folder manually. 
Atlas builds a single index across the folders **you choose** and sorts it by a "likely forgotten" heuristic (age + size) so the old, unused stuff actually surfaces instead of hiding in plain sight.

## What it does?

- Recursively scans one or more folders you choose
- Captures metadata only — path, size, extension, modified date (no file contents are read)
- Indexes everything into a local SQLite database
- Filters out system junk, caches, and temp files via a configurable exclusion list
- Sorts by likely-forgotten (oldest modified + size) so neglected files rise to the top
- Never modifies, moves, or deletes anything on your filesystem

## What it deliberately doesn't do (yet)?

- No duplicate detection by default — content hashing is a planned on-demand feature, not a core scan step
- No "last opened" tracking — Windows doesn't reliably expose this, so Atlas doesn't pretend to know it
- No automatic file actions (archive/delete) — read-only in this phase, by design
- No background/scheduled scanning or real-time file watching

## Status

**Proof of concept validated.** The CLI scan + index + exclusion-config pipeline works and has been run against real folders. UI is not built yet.

- [x] Phase 0 — CLI scan, SQLite index, exclusion config
- [ ] Phase 1 — UI: sortable/filterable table view
- [ ] Phase 2 — disk-usage treemap, mark-reviewed/dismiss
- [ ] Phase 3 — on-demand duplicate check (optional, scoped)

See [Solution Overview](../../wiki/Solution-Overview-NEW) for the full design writeup.

## Running it (current phase)

```bash
python scan.py "C:\Users\you\Desktop"
```

On first run this creates `atlas_config.json` next to the script with sensible default exclusions (edit it to add your own). Each run updates `atlas_index.db` and prints the 20 oldest-modified files found.

## Tech stack

- Python (standard library: `os.scandir`, `sqlite3`) for the scan/index core. 

- UI planned with `pywebview` — chosen over Electron/Tauri because this workload is I/O-bound, not compute-bound, so the priority is shipping a real version, not raw backend performance.

## Platform

- Windows-first. 
	- Handles OneDrive placeholder files, 
	- Junctions/Symlinks
	- Protected-folder permission errors without crashing the scan.
- Other OS support is a distant future for now.

## License

MIT — see [LICENSE](LICENSE) for details.