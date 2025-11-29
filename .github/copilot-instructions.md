# Copilot / AI Agent Instructions — PhotoApp

Quick, actionable guidance for AI coding agents working in this repository.

1. Project overview
- Purpose: local Windows desktop photo manager (PySide6 UI, SQLite backend).
- Key areas: `app.py` (entry), `src/core/` (domain logic), `src/services/` (orchestration/background jobs), `src/ui/` (PySide6 views/widgets), `data/` (DB + caches), `config/` (YAML settings).

2. How the app boots
- `app.py` adds `src/` to `sys.path`, loads config via `src.core.config.load_config()`, configures logging, calls `src.core.db.init_database(config)`, instantiates `JobManager` and starts the Qt `MainWindow`.
- Any agent-run code should mimic `load_config(repo_root)` to resolve paths relative to the repo (see `src/core/config.py`).

3. Configuration conventions
- Config model: `src/core/config.py` defines `AppConfig` (Pydantic). Modules often import `Config` (alias for `AppConfig`).
- Path resolution: relative paths in YAML are resolved against the repo root found by searching for `config/default.yaml` — use `load_config()` or `_resolve_path()` behavior when constructing file paths.
- Face recognition is opt-in: check `config.face_recognition.enabled` and `model_dir` before using `FaceEmbedder`.

4. Database patterns
- ORM: SQLAlchemy 2-style Declarative via `src/core/db.py` and `src/core/models.py`.
- Init: call `init_database(config)` to configure `engine` and `SessionLocal` and create tables.
- Use `get_session()` context manager for transactional work; it commits on success and rolls back on exceptions.

5. Background jobs and services
- `src/services/jobs.py` provides an in-memory `JobManager` — register handlers via `job_manager.register('type', handler)` and enqueue with `job_manager.enqueue(...)`.
- Indexing: `src/services/indexer.py` shows the canonical pipeline: query photos, extract EXIF (`src/core/exif.py`), update DB models, and call `src/core/thumbnails.ensure_thumbnails()`.
- Face indexing: `src/services/face_indexer.py` wraps `src/core/faces.FaceEmbedder` and expects `config.face_recognition.model_dir` to be present.

6. Common code patterns to follow
- Prefer `load_config(repo_root)` to obtain an `AppConfig` instance — tests and scripts use this.
- DB sessions: always use `with get_session() as session:` to ensure proper lifecycle.
- Thumbnail pipeline uses a small proxy object (SimpleNamespace) with `id`, `relative_path`, `root_path` — mirror this shape when calling `ensure_thumbnails()`.
- Batch processing: `process_photos_in_batches(..., batch_size, processor)` is used for progress logging; reuse its shape for long-running loops.

7. Tests and developer workflows
- Install dev deps: `pip install -e .[dev]` (project README).
- Init DB for local dev: `python scripts/init_db.py` (creates DB at `data/photos.db` by default).
- Run tests: `pytest -q` from repo root. Use the configured `src/` path (scripts add it automatically when launching `app.py`).

8. Useful one-off commands (PowerShell)
```powershell
# install dev deps
pip install -e .[dev]

# initialize DB
python .\scripts\init_db.py

# run the app
python .\app.py

# run tests
pytest -q
```

9. Files to read for implementation clues
- `src/core/config.py` — config merging and path resolution
- `src/core/db.py` and `src/core/models.py` — engine/session patterns and schema
- `src/services/indexer.py` — canonical indexing flow (EXIF -> thumbnails -> DB)
- `src/services/face_indexer.py` and `src/core/faces.py` — face detection/embedding entry points
- `app.py` and `src/ui/main_window.py` — how services are wired into the UI

10. What agents should not assume
- No external face model is bundled; face recognition is optional and requires `model_dir` configured.
- JobManager is in-memory and synchronous — for long-running tasks prefer using the provided batch helpers (no background worker infra exists yet).

If anything here is unclear or you'd like more examples (e.g., small code snippets for adding a job handler, or a walkthrough of the indexing flow), tell me which area and I'll expand with concrete edits or unit-testable examples.
