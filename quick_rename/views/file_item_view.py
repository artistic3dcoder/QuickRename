from PySide2.QtGui import QStandardItem, QColor, QFont
from PySide2.QtCore import Qt

from defaults import file_item_prefs as prefs

class FileItemView(QStandardItem):
    """View which represents a single file item.

    Attributes:
        controller (FileItemController): Controller responsible for view.
    """

    def __init__(self):
        super(FileItemView, self).__init__()
        self.controller = None
        self._configure()

    @property
    def name(self) -> str:
        """Label name associated with view"""
        return str(self.text())

    def _configure(self) -> None:
        """Configuration of FileItemView."""
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsDropEnabled)
        self.setEditable(False)
        self.setCheckState(Qt.Unchecked)

    def add_controller(self, controller: object) -> None:
        """Link a controller with this view.

        Args:
            controller: Controller responsible for view.
        """
        self.controller = controller

    def checked(self) -> bool:
        """Returns if the current QStandardItem is checked."""
        return self.checkState() == Qt.Checked

    def set_check_state(self, state: object) -> None:
        """set the check state of the view."""
        self.setCheckState(state)

    def set_label(self, label: str) -> None:
        """Set label on FileItemView.

        Args:
            label: Label applied to item.
        """
        self.setText(label)

    def set_invalid(self, state: bool) -> None:
        """Set the current item as invalid or valid.

        Args:
            state: invalid state of Item.
        """
        font = QFont()
        if state:
            self.setForeground(QColor(prefs.COLOR_INVALID))
            font.setWeight(QFont.Bold)
            font.setItalic(True)
        else:
            self.setForeground(QColor(prefs.COLOR_VALID))
            font.setWeight(QFont.Normal)
            font.setItalic(False)

        self.setFont(font)
