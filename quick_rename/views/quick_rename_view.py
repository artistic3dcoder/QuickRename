from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem

from defaults.css import CSS
from defaults import quick_rename_prefs as prefs


class QuickRenameView(QWidget):
    """Main view for QuickRename.

    Attributes:
        layout: Layout associated with QuickRenameView.
        folder_view: View which represents folder selection where renamable files live.
        limit_view: View which provides options for limiting what is renamed.
        file_view: View which provides an interface for renaming selected files.
        options_view: View which provides options which control how renaming is performed.
        buttons_view: View which provides buttons to trigger actions in rename process.
    """

    def __init__(self,
                 folder_view: object,
                 limit_view: object,
                 file_view: object,
                 options_view: object,
                 buttons_view: object):
        """Initialization of QuickRenameView.

        Args:
            folder_view: View which represents folder selection where renamable files live.
            limit_view: View which provides options for limiting what is renamed.
            file_view: View which provides an interface for renaming selected files.
            options_view: View which provides options which control how renaming is performed.
            buttons_view: View which provides buttons to trigger actions in rename process.
        """
        super(QuickRenameView, self).__init__()

        self.layout = QVBoxLayout()
        self.folder_view = folder_view
        self.limit_view = limit_view
        self.file_view = file_view
        self.options_view = options_view
        self.buttons_view = buttons_view
        self._instructions_layout = QHBoxLayout()
        self._instructions = QLabel(prefs.INSTRUCTIONS)

        self._configure()

    def _configure(self) -> None:
        """Configure QuickRenameView."""
        self.layout.setAlignment(Qt.AlignTop)
        self._instructions_layout.setAlignment(Qt.AlignCenter)
        self._instructions.setObjectName(prefs.INSTRUCTIONS_NAME)
        self._instructions_layout.addWidget(self._instructions)
        self.layout.addWidget(self.folder_view)
        self.layout.addWidget(self.limit_view)
        self.layout.addSpacerItem(QSpacerItem(*prefs.SPACING))
        self.layout.addLayout(self._instructions_layout)
        self.layout.addWidget(self.file_view)
        self.layout.addWidget(self.options_view)
        self.layout.addWidget(self.buttons_view)

        self.setWindowTitle(prefs.TITLE)
        self.setWindowIcon(QIcon("icons/quick_rename_icon.png"))
        self.setStyleSheet(CSS)
        self.setLayout(self.layout)
