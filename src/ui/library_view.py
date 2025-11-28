"""Library view with search and thumbnail grid."""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget

from src.ui.widgets.thumbnail_grid import ThumbnailGrid


class LibraryView(QWidget):
    """Displays the photo library with a search field and thumbnail grid."""

    searchTextChanged: Signal = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._search_input = QLineEdit(parent=self)
        self._search_input.setPlaceholderText("Search photos…")

        self.thumbnail_grid: ThumbnailGrid = ThumbnailGrid(parent=self)

        layout = QVBoxLayout()
        layout.addWidget(self._search_input)
        layout.addWidget(self.thumbnail_grid)
        self.setLayout(layout)

        self._search_input.textChanged.connect(self._on_search_text_changed)

    def search_text(self) -> str:
        """Return the current search query text."""

        return self._search_input.text()

    def set_search_text(self, text: str) -> None:
        """Set the search query text programmatically."""

        self._search_input.setText(text)

    @Slot(str)
    def _on_search_text_changed(self, text: str) -> None:
        self.searchTextChanged.emit(text)
