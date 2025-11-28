"""Main window definition for the Photo Manager application."""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QAction, QLabel, QMainWindow, QMenuBar


class MainWindow(QMainWindow):
    """Primary application window presenting the photo library."""

    def __init__(self, parent: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Photo Manager")
        self.resize(QSize(1024, 768))

        placeholder = QLabel("Library goes here", parent=self)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(placeholder)

        menu_bar = QMenuBar(parent=self)
        self._build_menus(menu_bar)
        self.setMenuBar(menu_bar)

    def _build_menus(self, menu_bar: QMenuBar) -> None:
        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction("E&xit", parent=self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menu_bar.addMenu("&View")
        library_action = QAction("&Library", parent=self)
        library_action.setEnabled(False)
        view_menu.addAction(library_action)

        tools_menu = menu_bar.addMenu("&Tools")
        tools_menu.addAction(QAction("&Reindex", parent=self))
