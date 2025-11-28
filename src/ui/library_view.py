"""Library grid view placeholder."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout

from src.core.config import Config


class LibraryView(QWidget):
    def __init__(self, config: Config, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config = config
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Library view will show thumbnails here."))
        self.setLayout(layout)
