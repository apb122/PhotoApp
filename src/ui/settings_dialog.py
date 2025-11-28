"""Settings dialog placeholder."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QLabel, QDialog, QVBoxLayout


class SettingsDialog(QDialog):
    def __init__(self, parent: Optional[QDialog] = None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings go here"))
        self.setLayout(layout)
