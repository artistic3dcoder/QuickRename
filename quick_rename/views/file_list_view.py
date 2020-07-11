from typing import Iterable, List
from PySide2.QtWidgets import QAbstractItemView, QHeaderView, QTableView
from PySide2.QtGui import  QStandardItemModel
from PySide2.QtCore import Qt

from controllers.file_item_controller import FileItemController
from defaults import file_list_prefs as prefs


class FileListView(QTableView):
    """
    CustomTable which inherits the QTableView Class.

    Notes:
        This implementation fixes an apparent issue with the QTableView where if you drag and drop internally
        The dragged item when dropped would overwrite the item it was dropped on and leave a hole in the table
        where the dragged item originates from.

    Attributes:
        model (QStandardItemModel): Model associated with FileListView.
        header (QHeaderView): Header associated with FileListView.
        controller (FileItemController): View controller for FileListView.
    """
    def __init__(self, controller: object):
        """Init method for FileListView.

        Args:
            controller: View controller for FileListView.
        """
        super(FileListView, self).__init__()
        self.model = QStandardItemModel(prefs.ITEM_ROWS, prefs.ITEM_COLS)
        self.header = self.horizontalHeader()
        self.controller = controller

        self._configure()

    def _configure(self) -> None:
        """Configure FileListView."""
        self.setModel(self.model)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalHeader().hide()
        self.model.setHorizontalHeaderLabels(prefs.HEADERS)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setMinimumHeight(prefs.MIN_HEIGHT)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropOverwriteMode(False)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.verticalHeader().setSectionsMovable(True)
        self.verticalHeader().setDragEnabled(True)
        self.verticalHeader().setDragDropMode(QAbstractItemView.InternalMove)

        self.header.setSectionResizeMode(QHeaderView.Stretch)

    def dropEvent(self, event) -> None:
        """Implementation of dropEvent to handle how we need to drop the item."""
        # The QTableWidget from which selected rows will be moved
        drop_row = self.model.itemFromIndex(self.indexAt(event.pos())).row()
        # Move item.
        for data in (x for x in event.source().selected_items() if x.text() and x.column() == 0):
            new_item = FileItemController(label=data.text())
            new_item.set_check_state(check_state=data.checkState())
            self.model.insertRow(drop_row, new_item.view)
        event.accept()

    def selected_items(self) -> List[object]:
        """Returns a list of selected items.

        Note:
            This is helper method we are adding to specifically help PySide know what is selected for drag and drop
            functionality.
        """
        selected_rows = []
        for index in self.selectedIndexes():
            item = self.model.itemFromIndex(index)
            for selected in selected_rows:
                if selected.text() == item.text():
                    break
            else:
                selected_rows.append(item)
        return selected_rows

    def all_items(self) -> Iterable:
        """Yield all file items from the file list column (first column)."""
        # Walk through the available rows and collect the items. Only collect items which are valid.
        for i in range(self.model.rowCount()):
            item = self.model.item(i, 0)
            if item:
                yield item

    def clear(self) -> None:
        """Clear the model."""
        self.model.clear()

    def clear_preview(self) -> None:
        """Clear items in the preview column."""
        # Walk through the rows and del all items found in the second column
        for i in range(self.model.rowCount()):
            item = self.model.takeItem(i, 1)
            if item:
                del item
        # Remove the preview column and then re-add a column. If we do not do this The View does not always refresh and
        # remove the items.
        self.model.removeColumn(1)
        self.model.setColumnCount(2)

    def get_checked_rows(self) -> Iterable:
        """Yield all rows in self.model and return checked items."""
        for i in range(self.model.rowCount()):
            item = self.model.item(i, 0)
            if item.checked():
                yield item

    def set_disabled(self) -> None:
        """Disable View."""
        self.setDisabled(True)

    def set_enable(self) -> None:
        """Enable View."""
        self.setEnabled(True)

    def set_header_labels(self, labels: List[str]) -> None:
        """Set header labels in view.

        labels: Labels applied to header.
        """
        self.model.setHorizontalHeaderLabels(labels)

    def set_item(self, row: int, col: int, item: object) -> None:
        """Add a FileItemView to the model.

        Args:
            row: Row to add item to.
            col: Column to add item to.
            item: Item to add to model.
        """
        self.model.setItem(row, col, item)

    def set_row_count(self, rows: int) -> None:
        """Set number of rows in view.

        Args:
            rows: Number of rows in view.
        """
        self.model.setRowCount(rows)
