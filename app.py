"""Entry point for the Photo Manager application."""
from __future__ import annotations

from pathlib import Path

from src.core.config import Config, load_config
from src.services.jobs import JobManager
from src.ui.main_window import launch


def main() -> None:
    """Initialize configuration, job manager, and start the Qt application."""
    project_root = Path(__file__).parent
    config = load_config(project_root)
    job_manager = JobManager()
    launch(config, job_manager)


if __name__ == "__main__":
    main()
