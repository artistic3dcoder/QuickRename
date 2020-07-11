from typing import List

from views.file_list_view import FileListView
from defaults import file_list_prefs as prefs


class FileListController(object):
    """Responsible for managing interactions with FileListView."""
    def __init__(self):
        self._view = FileListView(controller=self)

    @property
    def view(self) -> object:
        """View associated with FileListController"""
        return self._view

    def add_item(self, row: int, col: int, view: object) -> None:
        """Add an FileItemView to the FileListView."""
        self._view.set_item(row=row, col=col, item=view)

    def all_items(self) -> List[object]:
        """Return all file items from the file list column (first column)."""
        items = []
        for item in self._view.all_items():
            items.append(item)
        return items

    def clear(self) -> None:
        """Clear view."""
        self._view.clear()

    def clear_preview_column(self) -> None:
        """Clear items in the preview column."""
        self._view.clear_preview()

    def get_checked_files(self) -> List[object]:
        """Return all checked files for renaming."""
        checked_items = []
        for item in self._view.get_checked_rows():
            checked_items.append(item)
        return checked_items

    def get_checked_files_count(self) -> int:
        """Return the number of items that are checked for rename."""
        return len(list(self._view.get_checked_rows()))

    def set_disabled(self) -> None:
        """Disable View."""
        self._view.set_disabled()

    def set_enable(self) -> None:
        """Enable View."""
        self._view.set_enable()

    def set_header_labels(self) -> None:
        """Set header labels in view."""
        self._view.set_header_labels(labels=prefs.HEADERS)

    def set_row_count(self, rows: int) -> None:
        """Set number of rows in view.

        Args:
            rows: Number of rows in view.
        """
        self._view.set_row_count(rows=rows)
