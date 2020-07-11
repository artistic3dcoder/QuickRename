from typing import Union
from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QStandardItem, QColor, QFont

from defaults import file_item_prefs as prefs


class FileDirectoryDialog(QFileDialog):
    """FileDialog configured for selecting a directory.

    Attributes:
        options (QFileDialog.Options): Options associated with Dialog.
    """
    def __init__(self):
        super(FileDirectoryDialog, self).__init__()
        self.options = QFileDialog.Options()
        self._configure()

    def _configure(self) -> None:
        """Configure FileDirectoryDialog."""
        self.options |= QFileDialog.DontUseNativeDialog
        self.setOptions(self.options)

    def get_directory(self) -> Union[str, None]:
        """Show a directory dialog and return selected path."""
        result = self.getExistingDirectory()
        return str(result) if result else None


class Item(QStandardItem):
    """A QStandardItem with a bold font applied."""
    def __init__(self, label):
        """Initialization of the StandardItem."""
        super(Item, self).__init__()
        self.setText(label)
        self.setCheckable(False)
        self.setForeground(QColor(prefs.COLOR_INVALID))
        font = QFont()
        font.setWeight(QFont.Bold)
        font.setItalic(True)
        self.setFont(font)
