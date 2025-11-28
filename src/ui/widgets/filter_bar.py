"""Filter bar widget placeholder."""
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout


class FilterBar(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Filters"))
        self.setLayout(layout)
