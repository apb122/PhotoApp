"""Maintenance tools dialogs."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QLabel, QDialog, QVBoxLayout


class MaintenanceDialog(QDialog):
    def __init__(self, title: str, parent: Optional[QDialog] = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Maintenance job controls"))
        self.setLayout(layout)
