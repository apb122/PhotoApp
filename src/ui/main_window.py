"""Main window entry for the PySide6 application."""
from __future__ import annotations

import sys
from typing import Optional

from PySide6.QtWidgets import QApplication, QMainWindow

from src.core.config import Config
from src.services.jobs import JobManager
from src.ui.library_view import LibraryView


def launch(config: Config, job_manager: JobManager) -> None:
    app = QApplication(sys.argv)
    window = MainWindow(config=config, job_manager=job_manager)
    window.show()
    sys.exit(app.exec())


class MainWindow(QMainWindow):
    def __init__(self, config: Config, job_manager: JobManager, parent: Optional[QMainWindow] = None):
        super().__init__(parent)
        self.config = config
        self.job_manager = job_manager
        self.setWindowTitle("Photo Manager")
        self.view = LibraryView(config)
        self.setCentralWidget(self.view)
