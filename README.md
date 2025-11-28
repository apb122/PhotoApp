# Photo Manager Blueprint

This repository captures the initial architecture for a local-only Windows desktop photo manager built with Python, PySide6, and SQLite. The project is organized to separate core logic, orchestration services, and the Qt-based UI for easier maintenance and future expansion.

## Project layout
- `app.py`: Application entry point that loads configuration, initializes the job manager, and launches the Qt window.
- `config/`: Default and user-specific configuration in YAML.
- `data/`: Placeholder for the SQLite database, model files, and caches (thumbnails, faces, temp files).
- `logs/`: Application logs (rotating handlers to be added later).
- `src/core/`: Framework-agnostic logic for configuration, database access, hashing, EXIF parsing, thumbnails, faces, clustering, search, and helpers.
- `src/services/`: Workflows that orchestrate scanning, indexing, face processing, jobs, and backups.
- `src/ui/`: PySide6 UI surfaces (main window, views, dialogs, and custom widgets).
- `src/tests/`: Early unit tests for hashing, EXIF parsing, models, faces, and clustering utilities.
- `scripts/`: Developer helpers for database initialization, migrations, and benchmarking.

## Getting started
1. Install dependencies: `pip install -e .[dev]`
2. Initialize the database schema: `python scripts/init_db.py`
3. Launch the UI: `python app.py`

## Next steps
- Flesh out database models and persistence in `src/core/db.py` and `src/core/models.py`.
- Implement thumbnail caching logic and EXIF-driven metadata indexing in `src/services/indexer.py`.
- Wire InsightFace detection and clustering via `src/core/faces.py` and `src/core/clustering.py`.
- Expand the PySide6 UI views to present library browsing, people view, tags/albums, and maintenance tools.
