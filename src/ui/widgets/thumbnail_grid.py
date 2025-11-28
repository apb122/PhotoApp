"""Thumbnail grid widget placeholder."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout


class ThumbnailGrid(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Thumbnail grid"))
        self.setLayout(layout)
