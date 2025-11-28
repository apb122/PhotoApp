"""Thumbnail grid view for displaying photo thumbnails."""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QListView, QWidget


class ThumbnailGrid(QListView):
    """List view configured to present a grid of photo thumbnails."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._configure_view()

    def _configure_view(self) -> None:
        """Apply defaults suited for displaying image thumbnails."""

        self.setViewMode(QListView.ViewMode.IconMode)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setUniformItemSizes(True)
        self.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QListView.SelectionBehavior.SelectItems)
        self.setMovement(QListView.Movement.Static)
        self.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self.setSpacing(8)
        self.setIconSize(QSize(160, 160))
        self.setGridSize(QSize(176, 200))
        self.setVerticalScrollMode(QListView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QListView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
