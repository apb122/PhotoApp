"""Application entry point for Photo Manager."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

# Ensure project src directory is on sys.path when running as a script
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.core.config import Config, load_config  # noqa: E402
from src.core import db as db_module  # noqa: E402
from src.services.jobs import JobManager  # noqa: E402
from src.ui.main_window import MainWindow  # noqa: E402


def configure_logging(logs_dir: Path) -> None:
    """Configure application logging to file and stdout."""
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


def initialize_database(config: Config) -> None:
    """Initialize the SQLite database schema."""
    # Use the canonical init path on the DB module which creates engine,
    # session factory and tables.
    db_module.init_database(config)


def main() -> int:
    """Load configuration, initialize services, and start the Qt application."""
    config = load_config(PROJECT_ROOT)
    configure_logging(Path(config.logs_dir))
    initialize_database(config)

    job_manager = JobManager()
    app = QApplication(sys.argv)
    window = MainWindow(config=config, job_manager=job_manager)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
