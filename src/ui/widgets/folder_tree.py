"""Folder tree widget placeholder."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout


class FolderTree(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Folder tree"))
        self.setLayout(layout)
